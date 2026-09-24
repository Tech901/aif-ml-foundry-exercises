# Foundry Exercises — Models & Prompts

A two-part Codio assignment. Students explore the Microsoft Foundry model catalog
and answer a quiz about it, then write system and user prompts for three challenges
in the Prompt Lab, a web page that runs beside the guide and sends each prompt to
their own deployment. No code is written by students.

## Overview

| | |
| --- | --- |
| Duration | About 90 min |
| Students need | Their course Azure account and Foundry project, with a deployment named `memphis-copilot` (model `gpt-4.1-mini`); the setup page says how to make one if it is missing. |
| Students make | `.env` with their endpoint and key; three prompts, written in the Prompt Lab. |
| Parts | Set up your endpoint · Part 1, the model catalog and its quiz · Part 2, start the Prompt Lab · Challenges 1–3 · Wrap up |
| Grading | 1 endpoint check, 7 quiz questions (one attempt each) and 3 challenge checks, 20 points each. Challenge checks award partial credit on a 0–100 score with 70 as the pass mark; the best press is kept. |

The three challenges:

| # | Students write | Graded on |
| --- | --- | --- |
| 1 | System prompt | role/persona, scope and guardrails (an off-topic test message probes them), tone, output rules |
| 2 | User prompt (fixed system prompt) | context, one clear task, format and length, quality cues |
| 3 | System prompt (user prompt is a fixed trigger) | job definition, schema, robustness rules, and an automatic JSON format check over three messages |

## Instructor setup, before publishing to Codio

1. **Student deployments.** `memphis-copilot` at 100,000 TPM per student; check the
   `gpt-4.1-mini` quota in East US 2 covers the class.
2. **Stack.** `openai` and `python-dotenv` from the course stack; `lab.sh` installs
   Flask for the student on first start if the stack lacks it.
3. **`.env`.** Ships blank in git with `AI901_ENDPOINT` and `AI901_KEY`. It is gitignored so a filled-in copy is not staged by
   accident; in any clone you work in, run `git update-index --skip-worktree .env` once.
4. **Quiz drift.** The Part 1 questions were written against durable catalog facts,
   but the catalog evolves; give them a quick pass each term.
5. **Publish** after any grader change, bumping the guide version line on the
   Overview page.

## Delivery guide

The setup, Part 1 and the start of the Prompt Lab are presented by the instructor,
live. The three challenges are done by students on their own.

| Minutes | Segment | What to do |
| --- | --- | --- |
| 0–10 | Overview, Set up your endpoint | Confirm everyone has `memphis-copilot`. Fill `.env` from the detail panel with the pictures; the check proves it. |
| 10–35 | Part 1 | Open the catalog together and show the search, the filters and a model card. Then students answer the seven questions; each has one attempt, so say so before the first. |
| 35–45 | Part 2, Start the Prompt Lab | Start the test bed once; show the brief, the editor, Run, and the cards. Explain that the page saves as they type and the Check button grades what was saved. |
| 45–85 | Challenges 1–3 (students alone) | Circulate. Push students to read replies against the requirements before pressing Check. Challenge 3's format check lines are the fastest feedback loop. |
| 85–90 | Wrap up | Best scores are already recorded; Mark as complete submits. |

What to watch for:

- A pasted-from-the-brief prompt scores zero by design. The message says why.
- Challenge scores come from a model judge and vary a little between presses; the
  best is kept, so press again.
- The Prompt Lab starts on the Part 2 page only; every challenge page has a reopen
  link if the box restarted.

## How grading works

Every button is a Codio Advanced Code Test running
`python3 .guides/secure/run.py <check-id>`. `run.py` loads the student's endpoint and
key from `.env`, scrubs the key from all output, and dispatches to `check_graded.py`:

- `check-env` sends one question to `memphis-copilot` and passes when it answers.
- `check-challenge-N` reads the prompt the Prompt Lab saved to
  `prompts/challenge_<id>.json`, runs it against the challenge's test messages,
  applies the JSON format check for challenge 3, then asks the same deployment to
  score the prompt against the rubric. The harness clamps each criterion to its
  maximum and totals it itself, and reports the total as the percent.
- An empty prompt, or one pasted from the brief (five-word overlap with the
  challenge text), scores zero without a model call.

Nothing a student can write is trusted as a score: the saved file holds only the
prompt, which the grader re-runs and re-scores.

## Project layout

```
.codio                     Run menu: start/restart/stop the Prompt Lab, test the connection
.guides/
  assessments/             7 multiple-choice quiz items + 4 Advanced Code Tests
  content/                 Guide pages
  img/                     Illustrations for the .env page
  secure/run.py            Grader harness (credentials, scrubbing, dispatch)
  secure/check_graded.py   The four checks
app.py                     The Prompt Lab test bed (Flask, port 5000)
lab.sh                     start / stop / restart / status / prepare for the Prompt Lab
templates/, static/        The Prompt Lab page
challenges.json            Briefs, rubrics, test messages, pass score
test_connection.py         Terminal connection check
.env                       Ships blank; students fill it in
```
