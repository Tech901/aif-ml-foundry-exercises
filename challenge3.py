"""Challenge 3 - Structured output. You write the SYSTEM PROMPT; the user prompt is a trigger.

Bluff City Bikes gets support emails and wants to log them automatically. Your system
prompt must make the model read a customer message and return ONLY a JSON object with
exactly these keys:

    customer_name, product, issue, sentiment, urgency

with sentiment one of positive / neutral / negative and urgency one of low / medium /
high. Say what to do when a detail is missing (use null, never drop the key) and forbid
any text or markdown code fences around the JSON.

USER_PROMPT is filled in for you. It is only the trigger that hands over each customer
message; you may edit it, but the rules belong in SYSTEM_PROMPT.

The Check button in the guide runs your prompts against three customer messages (one
complete, one with details missing, one full of numbers), checks every reply's JSON
automatically, and grades the prompts 0-100 against the rubric on the guide page.
70 passes; your best score is kept.
"""

SYSTEM_PROMPT = """
Write your system prompt here, replacing this line.
"""

USER_PROMPT = "Log this customer message for our support system."


if __name__ == "__main__":
    # Optional: run this file from a terminal to see the replies without grading.
    from prompt_tools import try_it
    try_it(challenge=3, system_prompt=SYSTEM_PROMPT, user_prompt=USER_PROMPT)
