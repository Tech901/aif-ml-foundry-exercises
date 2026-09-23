"""Challenge 2 - Sharpen the ask. You write the USER PROMPT.

A neighborhood association wants a piece of writing that encourages residents to
recycle correctly. Someone typed "write something about recycling" into the model and
got a generic wall of text. Write the user prompt they should have written.

The system prompt is fixed and plain ("You are a helpful writing assistant."), so
everything has to come from USER_PROMPT below: who is asking and why, one specific
piece of writing, its audience, length and format, the tone, and at least one thing it
must include or avoid. Invent the real specifics; a prompt that only restates that
checklist scores zero.

The Check button in the guide sends your prompt once and grades the result 0-100
against the rubric on the guide page. 70 passes; your best score is kept. Nothing else
in this file needs to change.
"""

USER_PROMPT = """
Write your user prompt here, replacing this line.
"""


if __name__ == "__main__":
    # Optional: run this file from a terminal to see the reply without grading.
    from prompt_tools import try_it
    try_it(challenge=2, user_prompt=USER_PROMPT)
