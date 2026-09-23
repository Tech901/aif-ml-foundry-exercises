"""Challenge 1 - Coach the assistant. You write the SYSTEM PROMPT.

Bluff City Bikes is a small bicycle shop in Memphis. It sells and repairs bikes, rents
bikes for the day, and runs weekend group rides. The shop wants an assistant for its
website chat widget.

Write SYSTEM_PROMPT below: everything between the two lines of three quote marks is
the prompt. It should give the assistant a role and a name, keep it on bike-shop
subjects, set a friendly tone for people who know nothing about bikes, and add at
least one concrete output rule.

The Check button in the guide sends your prompt to the model with two customer
messages, one on-topic and one off-topic, and grades the result 0-100 against the
rubric on the guide page. 70 passes; your best score is kept. Nothing else in this
file needs to change.
"""

SYSTEM_PROMPT = """
Write your system prompt here, replacing this line.
"""


if __name__ == "__main__":
    # Optional: run this file from a terminal to see the replies without grading.
    from prompt_tools import try_it
    try_it(challenge=1, system_prompt=SYSTEM_PROMPT)
