# Part 2 — Start the Prompt Lab

Part 2 happens in one web page, the **Prompt Lab**. It shows each challenge's brief on the left and a place to write your prompt on the right, sends the prompt to your `memphis-copilot` deployment when you press Run, and shows what came back. You write no code: the page does the sending, and the Check button on each challenge page does the grading.

1. Opening this step started the Prompt Lab in the background and opened its page in a tab beside this guide, along with a small terminal that reports its progress. The tab is white while the server starts; wait for the terminal to say `Prompt Lab running on port 5000`, then press the refresh arrow at the top left of the tab if it has not filled in on its own.

2. Look at the page once it loads. It is already on Challenge 1. The left side holds the brief: the scenario, what your prompt must do, and the rubric the Check button will use. The right side holds the editor for the prompt you write, the fixed text you do not write shown read-only, and the **Run my prompts** button. Under the button, each run appears as a card with the model's replies, newest on top.

3. Two habits to form now. Your prompt is saved as you type, so there is nothing to submit from the page; the Check button on the guide grades whatever the page last saved. And a red card is the page naming what went wrong, usually a value in `.env`; read it before changing anything.

4. Leave the tab open and go on to Challenge 1. The server keeps running from page to page; the later pages reopen the tab on their own challenge, they do not start anything. If the tab ever goes missing or shows a connection error, come back to this step, or press the link below.

[Start or reopen the Prompt Lab](cmd bash lab.sh start; open_preview https://{{domain5000}}/challenge/1 panel=1)

> **Checkpoint:** The terminal says `Prompt Lab running on port 5000`, and the page shows Challenge 1 with an empty system prompt editor. If a banner across the top says the page is not configured, `.env` is missing a value; fix it on the Set up your endpoint page, save, and the banner clears on its own within a few seconds.
