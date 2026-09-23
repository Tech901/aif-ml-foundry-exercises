# Challenge 2 — Sharpen the ask

**Skill: writing a user prompt.** Most disappointing AI answers come from prompts like the one you are about to fix:

> *write something about recycling*

The model cannot read minds, so it fills every gap with a guess. A strong user prompt closes the gaps. A reliable recipe:

| Ingredient | Answers the question | Example |
| --- | --- | --- |
| **Context** | Who is asking, and why? | "I'm writing for our neighborhood association ..." |
| **Task** | What exactly do you want? | "... draft a one-page flyer ..." |
| **Format** | What should it look like? | "... a headline, 3 bullet do's and don'ts, under 150 words ..." |
| **Quality cues** | Tone? Include or avoid? | "... friendly, no guilt-tripping, end with a call to action." |

### The scenario

A neighborhood association wants a piece of writing that encourages residents to recycle correctly. Someone on the team typed the vague request above into the model and got a generic wall of text. Your job is to write the user prompt they should have written.

### Your job

The Prompt Lab beside this page shows Challenge 2. Write in its **User prompt** editor. The system prompt is fixed and plain, "You are a helpful writing assistant.", so everything has to come from your user prompt:

- **Context.** Who is asking and why: the association and its goal.
- **One task.** The kind of writing you want, such as a flyer, an email or a social post.
- **Constraints.** Audience, length and format: headings, bullets, word limits.
- **Quality cues.** The tone to use, and at least one thing the writing must include, such as three do's and don'ts or a call to action, or must avoid.

> **Do not paste the checklist.** Those bullets describe what a good prompt *contains*; they are not the prompt. A prompt that says "provide context and specify a format" scores zero. Invent the actual specifics yourself: who the flyer is for, what it must say, how long it can be.

### The rubric

| Criterion | Points | What earns them |
| --- | --- | --- |
| Context and purpose | 25 | The prompt explains who it is for and what it is trying to achieve. |
| One clear task | 25 | The prompt asks for one specific, unambiguous deliverable. |
| Format and length | 25 | The prompt constrains audience, structure and length, and the reply respects them. |
| Quality cues | 25 | The prompt sets tone and names concrete content to include or avoid. |

### Have it checked

Press **Run my prompts** in the Prompt Lab and compare the reply with what "write something about recycling" would get: a specific prompt produces something the association could print. When it does, press the button below to have the prompt graded. 70 passes; your best score is kept.

If the Prompt Lab tab beside this page is blank or shows a connection error, press this once: [Start or reopen the Prompt Lab](cmd bash lab.sh start; open_preview https://{{domain5000}}/challenge/2 panel=1)


{Check challenge 2|assessment}(test-561208473)

> **Checkpoint:** The first line of the result reads `PASSED`. The reply is the piece of writing you asked for, in the format and length you set, not an essay about recycling in general.
