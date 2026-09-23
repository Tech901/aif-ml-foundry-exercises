# Part 2 — How the challenges work

The next three pages each open one small Python file beside the guide: `challenge1.py`, `challenge2.py`, `challenge3.py`. Each file holds a prompt as a block of text between two lines of three quote marks, with a placeholder line inside. You replace the placeholder with your prompt and save. Nothing else in the file needs to change.

### What the Check button does

Each challenge page has one **Check** button. A press does three things:

1. **Runs your prompt.** It sends your prompt to your `memphis-copilot` deployment with the challenge's test messages, and shows you every reply.
2. **Checks the format** where the challenge has one. Challenge 3 wants JSON, so each reply is parsed and its keys and values are verified before any opinion is formed.
3. **Grades the prompt.** The model is asked to score your prompt, not its own replies, against the rubric printed on the challenge page, and to write two or three specific edits that would improve it.

The first line of the result reads `PASSED` at 70 or more, or `NOT YET` with the score. The score is the share of the challenge's points you earn, and Codio keeps your best one, so a worse attempt never costs you anything.

### The rhythm

Edit the prompt, press Check, read the replies and the improvements, edit again. Nobody writes the right prompt on the first attempt, and the improvements are written as edits you can make directly. Two things the grader will not reward: a prompt left at its placeholder, and a prompt that pastes the challenge's own requirements back as instructions. Write the actual request, with the real specifics.

If you want to see replies without a grade, a terminal will do it: `python3 challenge1.py` runs the same test messages and prints what came back.

Ready? On to Challenge 1.
