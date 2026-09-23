# Foundry Exercises — Models & Prompts

A two-part Codio assignment for the AI fundamentals course.

1. **Part 1 — Explore the model catalog.** Students browse the Microsoft Foundry
   model catalog and answer a seven-question multiple-choice quiz whose answers
   are only in the catalog (publishers, inference tasks, model cards, deployment
   options).
2. **Part 2 — Write the prompts.** Students write a system prompt, a user prompt,
   and a JSON-extraction system prompt in the **Prompt Lab**, a small Flask page
   that runs beside the guide as the assignment's test bed. Run sends the prompt
   to the student's own `memphis-copilot` deployment and shows the replies; a
   Check button on each guide page grades the saved prompt 0–100 against a rubric.
   No code is written by students.

## The three challenges

| # | Students write | Graded on |
| --- | --- | --- |
| 1 | System prompt | role/persona, scope and guardrails (an off-topic test message probes them), tone, output rules |
| 2 | User prompt (fixed system prompt) | context, one clear task, format and length, quality cues |
| 3 | System prompt (user prompt is a fixed trigger) | job definition, schema, robustness rules, and an automatic JSON format check over three messages |

## How it fits together

- **The Prompt Lab (`app.py`)** is the test bed, started the way every lab's test
  bed is: the setup page runs `bash lab.sh prepare` in a small terminal while the
  student fills in `.env`, the Start page runs `bash lab.sh start` and opens the
  preview, and the challenge pages only reopen the preview on their own challenge.
  It re-reads `.env` on every request, saves the student's prompt to
  `prompts/challenge_<id>.json` as they type and on every Run, and shows each Run
  as a card, newest on top, with the challenge 3 format check underneath. It does
  not grade.
- **The Check buttons** are standard Codio Advanced Code Tests running
  `python3 .guides/secure/run.py <check-id>`. `run.py` loads the student's endpoint
  and key from `.env`, scrubs the key from all output, and dispatches to
  `check_graded.py`:
  - `check-env` sends one question to `memphis-copilot` and passes when it answers.
  - `check-challenge-N` reads the saved prompt, runs it against the challenge's
    test messages, applies the JSON format check for challenge 3, then asks the
    same deployment to score the prompt against the rubric. The harness clamps
    each criterion to its maximum and totals it itself, and reports the total as
    the percent, so partial points are earned below the pass mark and Codio keeps
    the best score. An empty prompt, or one pasted from the brief (measured by
    five-word overlap with the challenge text), scores zero without a model call.
- Nothing a student can write is trusted as a score: the saved prompt file only
  holds the prompt, which the grader re-runs and re-scores. Scores come from a
  model judge, so they vary a little between presses; the best is kept.

Challenge definitions (scenario, requirements, rubric, test messages, pass
score) live in `challenges.json`; the Prompt Lab renders them and the guide pages
repeat them, so edit all three together.

## Project layout

```
.codio                     Run menu: start/restart/stop the Prompt Lab, test the connection
.guides/
  assessments/             7 multiple-choice quiz items + 4 Advanced Code Tests
  content/                 Guide pages (Codio book format)
  img/                     Illustrations for the .env page
  secure/run.py            Grader harness (credentials, scrubbing, dispatch)
  secure/check_graded.py   The four checks
app.py                     The Prompt Lab test bed (Flask, port 5000)
lab.sh                     start / stop / restart / status / prepare for the Prompt Lab
templates/, static/        The Prompt Lab page
challenges.json            Briefs, rubrics, test messages, pass score
test_connection.py         Terminal connection check (the guide's check button does the same)
.env                       Per-student endpoint and key (ships blank; students fill it in)
```

## For instructors

- **Environment.** The course stack ships `openai` and `python-dotenv`; `lab.sh`
  installs Flask for the student on first start if the stack lacks it.
- **Students need** a deployment named `memphis-copilot` (model `gpt-4.1-mini`)
  in their Foundry project. The Set up your endpoint page tells them how to
  deploy one if it is missing, and records a check when it answers.
- **Grader changes** only reach students through a Codio publish. Bump the
  guide version line on the Overview page with every grader change so the
  assignment has a visible change to publish.
- **Catalog drift.** The Part 1 questions were written against durable facts,
  but the catalog evolves; give the quiz a quick pass each term.
