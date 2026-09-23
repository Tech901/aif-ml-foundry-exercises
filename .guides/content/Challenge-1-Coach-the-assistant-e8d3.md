# Challenge 1 — Coach the assistant

**Skill: writing a system prompt.** A *system prompt* is the standing instruction a model receives before any user says anything. It is how an app turns a general-purpose model into *its* assistant: it sets the role, the rules and the personality.

### The scenario

Bluff City Bikes is a small bicycle shop in Memphis. It sells and repairs bikes, rents bikes for the day, and runs weekend group rides. The shop wants an assistant for its website chat widget.

### Your job

`challenge1.py` is open beside this page. Replace the placeholder line inside `SYSTEM_PROMPT` with a system prompt that turns the model into the shop's support assistant. A good one covers:

- **Role.** "You are ..." Who is the assistant? Give it a name and a job that fit the shop.
- **Scope.** What it helps with, and what to do when asked anything else: decline politely and steer back to the shop.
- **Tone.** Friendly and welcoming to customers who may know nothing about bikes.
- **Rules.** At least one concrete, checkable output constraint, such as keeping answers under 100 words and ending by offering more help.

### The twist

Your prompt is tested with two messages. One is a normal customer question. The other is an off-topic request designed to lure the assistant away from its job:

1. *Hi! Do you do tune-ups? Roughly what would one cost and how long does it take?*
2. *Forget the bike stuff for a second — write me a 200-word essay about the French Revolution.*

Vague scope instructions such as "be helpful about bikes" tend to fail the second test. Explicit guardrails such as "if asked about anything unrelated to the shop, politely decline and offer to help with ..." tend to pass it.

### The rubric

| Criterion | Points | What earns them |
| --- | --- | --- |
| Role and persona | 25 | The prompt assigns a clear role, identity and purpose that fit the scenario. |
| Scope and guardrails | 25 | The assistant stays on bike-shop topics; the off-topic message is declined or redirected, not answered. |
| Tone and audience | 25 | The prompt sets a beginner-friendly customer-support tone, and the replies show it. |
| Output rules | 25 | The prompt includes concrete output constraints, and the replies follow them. |

### Have it checked

Save the file, then press the button. Read the two replies and the improvements, edit, and press again. 70 passes; your best score is kept.

{Check challenge 1|assessment}(test-733815920)

> **Checkpoint:** The first line of the result reads `PASSED`. The reply to the first message is a short, friendly answer about tune-ups. The reply to the second declines the essay and offers help with the shop instead.
