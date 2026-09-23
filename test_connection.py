"""Quick connection check for the Foundry Exercises.

Run from a terminal:  python3 test_connection.py

Reads your .env, sends one tiny request to the memphis-copilot deployment, and says
what to fix if anything is wrong. The guide's "Check the endpoint and key" button does
the same thing and records the result.
"""
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ENDPOINT = os.environ.get("AI901_ENDPOINT", "").strip()
KEY = os.environ.get("AI901_KEY", "").strip()
DEPLOYMENT = "memphis-copilot"


def fail(*lines):
    for line in lines:
        print(line)
    print("\nFix the value in .env, save, and run this again.")
    sys.exit(1)


missing = [name for name, value in (("AI901_ENDPOINT", ENDPOINT), ("AI901_KEY", KEY)) if not value]
if missing:
    fail("The .env file is missing a value for: " + ", ".join(missing),
         "Open .env, paste the value from the deployment's Details tab after the = sign, and save.")
if not ENDPOINT.startswith("https://") or not ENDPOINT.endswith("/"):
    fail("AI901_ENDPOINT must start with https:// and end with a slash.",
         f"You have: {ENDPOINT}")

print(f"Calling {DEPLOYMENT} ...")
try:
    client = OpenAI(base_url=f"{ENDPOINT}openai/v1/", api_key=KEY)
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[{"role": "user", "content": "Reply with exactly: Connection successful"}],
    )
except Exception as exc:  # noqa: BLE001
    text = str(exc).replace(KEY, "[key hidden]")
    if "401" in text or "403" in text:
        fail("The endpoint refused the key (HTTP 401/403). Copy the key from the Details tab again.")
    if "404" in text:
        fail(f"No deployment named {DEPLOYMENT} answered (HTTP 404). Check Build > Deployments in the portal,",
             "and that AI901_ENDPOINT is the host only, ending in a slash.")
    fail("The request failed:", "  " + text)

print("Success. The model replied:", (response.choices[0].message.content or "").strip())
print("Everything works. Go on with the assignment.")
