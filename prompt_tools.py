"""prompt_tools.py - written for you. Runs a challenge's prompts and prints the replies.

Each challenge file ends with a call to try_it(). Run the file from a terminal to see
what the model says to your prompt without grading it:

    python3 challenge1.py

The Check button in the guide does the same run, then grades the prompts. You do not
edit this file.
"""
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ENDPOINT = os.environ.get("AI901_ENDPOINT")
KEY = os.environ.get("AI901_KEY")
DEPLOYMENT = "memphis-copilot"     # the deployment name your requests carry, not the model's name

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenges.json"), encoding="utf-8") as fh:
    CHALLENGES = {c["id"]: c for c in json.load(fh)["challenges"]}


def ask(system_prompt, user_prompt):
    """One request: a system prompt and a user prompt in, the reply text out."""
    if not ENDPOINT or not KEY:
        sys.exit("No endpoint or key. Fill in the two lines in .env first (Set up your endpoint page).")
    client = OpenAI(base_url=f"{ENDPOINT}openai/v1/", api_key=KEY)
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt}],
    )
    return response.choices[0].message.content or ""


def try_it(challenge, system_prompt=None, user_prompt=None):
    """Run the prompts the way the Check button does, and print each reply."""
    spec = CHALLENGES[challenge]
    if spec["write"] == ["system"]:
        runs = [(system_prompt, m, m) for m in spec["test_messages"]]
    elif spec["write"] == ["user"]:
        runs = [(spec["fixed_system_prompt"], user_prompt, user_prompt)]
    else:
        runs = [(system_prompt, f"{user_prompt}\n\n--- Customer message ---\n{a['text']}", a["label"])
                for a in spec["attachments"]]
    for system, user, label in runs:
        print("=" * 60)
        print(label)
        print("-" * 60)
        print(ask(system, user))
    print("=" * 60)
    print("That is what the model said. Press the Check button in the guide to have it graded.")
