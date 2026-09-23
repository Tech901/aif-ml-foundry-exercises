#!/usr/bin/env python3
"""Foundry Exercises grader harness. Runs ONLY inside Codio's grading container.

Every Check button on the guide is an Advanced Code Test whose command is

    python3 .guides/secure/run.py <check-id>

The checks live in check_graded.py, which exposes CHECKS = {check_id: fn(creds)}.
This file loads the student's own endpoint and key from the .env file in the
workspace root, dispatches, and keeps the rules every lab in this course follows:
  * the key is never printed - every byte of student-visible output is scrubbed
  * failures are classified for the student, never dumped as a bare traceback
  * nothing is written into the student's workspace
  * all feedback is PLAIN TEXT - the student result panel does not render markdown
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE = HERE.parents[2]            # <workspace>/.guides/secure/run.py
STUDENT_ENV_FILE = WORKSPACE / ".env"

STEP_TIMEOUT = 60   # seconds for reading a student's file; the assessment timeout is 300
RULE = "-" * 40     # the student result panel is narrow


# --------------------------------------------------------------------------- codio
def send(percent: int, feedback: str) -> int:
    """Report score + PLAIN-TEXT feedback; exit 0 only on a full score."""
    percent = max(0, min(100, int(percent)))
    sent = False
    try:
        sys.path.append("/usr/share/codio/assessments")
        from lib.grade import FORMAT_V2_TXT, send_partial_v2  # type: ignore
        sent = bool(send_partial_v2(percent, feedback, FORMAT_V2_TXT))
    except Exception:
        sent = False
    if not sent:
        print(feedback)
    return 0 if percent >= 100 else 1


def load_creds() -> dict[str, str]:
    """Read AI901_ENDPOINT and AI901_KEY from the student's own .env file."""
    if not STUDENT_ENV_FILE.is_file():
        sys.exit(send(0, "No .env file found in your workspace root. It ships with the "
                         "assignment and the Set up your endpoint page fills it in. The "
                         "file must be named exactly .env (not .env.txt)."))
    creds: dict[str, str] = {}
    for line in STUDENT_ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        creds[k.strip()] = v.strip().strip('"').strip("'")
    missing = [k for k in ("AI901_ENDPOINT", "AI901_KEY") if not creds.get(k)]
    if missing:
        sys.exit(send(0, f"Your .env file is missing a value for {', '.join(missing)}. "
                         "Open it and paste the value from the portal after the = sign, "
                         "with no spaces."))
    ep = creds["AI901_ENDPOINT"]
    if not ep.startswith("https://") or not ep.endswith("/"):
        sys.exit(send(0, "AI901_ENDPOINT in your .env file must start with https:// and "
                         "end with a slash, exactly as the Set up your endpoint page shows "
                         "it. Fix the value and press the button again."))
    return creds


def scrub(text: str, creds: dict[str, str]) -> str:
    key = creds.get("AI901_KEY", "")
    if text and key and len(key) >= 8:
        return text.replace(key, "[key hidden]")
    return text


def classify(stderr: str) -> str | None:
    """Turn a failure into one sentence the student can act on."""
    s = stderr or ""
    if "429" in s or "RateLimitError" in s:
        return ("Your deployment is rate-limited (HTTP 429). Wait 60 seconds and press "
                "the button again.")
    if "401" in s or "403" in s or "AuthenticationError" in s or "PermissionDenied" in s:
        return ("The endpoint refused the key (HTTP 401/403). Check AI901_KEY in your .env "
                "file against the Details tab in the portal, and check the endpoint ends "
                "with a slash.")
    if "404" in s or "NotFoundError" in s or "DeploymentNotFound" in s:
        return ("The deployment name was not found (HTTP 404). This assignment sends to a "
                "deployment named memphis-copilot; the Set up your endpoint page says how "
                "to make one if your project has none.")
    if "APIConnectionError" in s or "Name or service not known" in s or "ConnectError" in s:
        return ("The endpoint could not be reached. Check AI901_ENDPOINT in your .env "
                "file, then press the button again.")
    if "No module named 'dotenv'" in s or "No module named 'openai'" in s:
        return ("A package is missing here. Assignment setup problem - tell your "
                "instructor (the stack should already include it).")
    if "SyntaxError" in s:
        return ("Python could not read your file (SyntaxError). Look at the line number "
                "in the message below - a quote mark inside your prompt, or a missing "
                "closing triple quote, is the usual cause.")
    if "NameError" in s:
        return ("A name in your file is not defined (NameError). Check spelling and "
                "capital letters.")
    return None


# The one-line program that reads the student's prompt constants. It runs in a
# subprocess from the workspace root so `import challenge1` resolves to the student's
# own file, and so a top-level error in that file cannot end the grader.
READ_PROMPTS = ("import sys, json, importlib; m = importlib.import_module(sys.argv[1]); "
                "print(json.dumps({'system': getattr(m, 'SYSTEM_PROMPT', None), "
                "'user': getattr(m, 'USER_PROMPT', None)}))")


def read_prompts(module: str, creds: dict[str, str]) -> tuple[dict | None, str]:
    """Import <workspace>/<module>.py in a subprocess and return its prompt constants.

    Returns (prompts, error). AI901_* is popped from the environment so nothing the
    grader holds can reach the student's code.
    """
    path = WORKSPACE / f"{module}.py"
    if not path.is_file():
        return None, f"{module}.py is missing from your workspace"
    env = os.environ.copy()
    env.pop("AI901_ENDPOINT", None)
    env.pop("AI901_KEY", None)
    env.update({"PYTHONUNBUFFERED": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    try:
        r = subprocess.run([sys.executable, "-c", READ_PROMPTS, module], cwd=str(WORKSPACE),
                           env=env, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=STEP_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, f"{module}.py did not finish loading within {STEP_TIMEOUT} seconds"
    if r.returncode != 0:
        tail = "\n".join(scrub(r.stderr, creds).strip().splitlines()[-6:])
        hint = classify(tail) or f"{module}.py could not be loaded."
        return None, f"{hint}\n\n{block(tail)}"
    import json
    for line in reversed(r.stdout.strip().splitlines()):
        try:
            return json.loads(line), ""
        except json.JSONDecodeError:
            continue
    return None, f"{module}.py loaded but its prompts could not be read."


def block(text: str, title: str = "") -> str:
    head = f"{title}\n" if title else ""
    return f"{head}{RULE}\n{text.rstrip()}\n{RULE}"


# --------------------------------------------------------------------------- modes
def _load_checks() -> dict:
    sys.path.insert(0, str(HERE.parent))
    try:
        return __import__("check_graded").CHECKS
    except Exception as exc:
        print(f"[grader] could not load check_graded: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return {}


def main(argv: list[str]) -> int:
    checks = _load_checks()
    if len(argv) != 2 or argv[1] not in checks:
        print(f"usage: run.py <{'|'.join(sorted(checks))}>", file=sys.stderr)
        return 2
    return checks[argv[1]](load_creds())


if __name__ == "__main__":
    sys.exit(main(sys.argv))
