# Foundry Exercises — Models & Prompts

A two-part Codio assignment for the AI fundamentals course.

1. **Part 1 — Explore the model catalog.** Students browse the Microsoft Foundry
   model catalog and answer a seven-question multiple-choice quiz whose answers
   are only in the catalog (publishers, inference tasks, model cards, deployment
   options).
2. **Part 2 — Write the prompts.** Students write a system prompt, a user prompt,
   and a JSON-extraction system prompt in three small Python files, and a Check
   button on each page runs the prompt against their own `memphis-copilot`
   deployment and grades it 0–100 against a rubric with concrete refinements.

## The three challenges

| # | File | Students write | Graded on |
| --- | --- | --- | --- |
| 1 | `challenge1.py` | `SYSTEM_PROMPT` | role/persona, scope and guardrails (an off-topic test message probes them), tone, output rules |
| 2 | `challenge2.py` | `USER_PROMPT` | context, one clear task, format and length, quality cues |
| 3 | `challenge3.py` | `SYSTEM_PROMPT` (user prompt is a fixed trigger) | job definition, schema, robustness rules, and an automatic JSON format check over three messages |

## How grading works

Every button on the guide is a standard Codio Advanced Code Test running
`python3 .guides/secure/run.py <check-id>`. `run.py` loads the student's own
endpoint and key from `.env`, scrubs the key from all output, and dispatches to
`check_graded.py`:

- `check-env` sends one question to `memphis-copilot` and passes when it answers.
- `check-challenge-N` reads the prompt constants out of the student's file in a
  subprocess, runs them against the challenge's test messages, applies the
  JSON format check for challenge 3, then asks the same deployment to score the
  prompts against the rubric. The harness clamps each criterion to its maximum
  and totals it itself. The total is reported as the percent, so partial points
  are earned below the pass mark and Codio keeps the best score.
- A prompt left at its placeholder, or one pasted from the brief (measured by
  five-word overlap with the challenge text), scores zero without a model call.

Nothing is read from files the student can write, so grades cannot be forged by
editing a results file. Scores still come from a model judge, so they vary a
little between presses; the best is kept.

Challenge definitions (scenario, requirements, rubric, test messages, pass
score) live in `challenges.json`. The guide pages repeat them for students, so
edit both together.

## Project layout

```
.codio                     Run menu: run the current file, test the connection
.guides/
  assessments/             7 multiple-choice quiz items + 4 Advanced Code Tests
  content/                 Guide pages (Codio book format)
  img/                     Illustrations for the .env page
  secure/run.py            Grader harness (credentials, scrubbing, dispatch)
  secure/check_graded.py   The four checks
challenge1.py, challenge2.py, challenge3.py   What students edit
prompt_tools.py            Written for you: runs a challenge's prompts from a terminal
challenges.json            Briefs, rubrics, test messages, pass score
test_connection.py         Terminal connection check (the guide's check button does the same)
.env                       Per-student endpoint and key (ships blank; students fill it in)
```

## For instructors

- **Environment.** The course stack already ships `openai` and `python-dotenv`;
  `requirements.txt` records them for a box that predates it.
- **Students need** a deployment named `memphis-copilot` (model `gpt-4.1-mini`)
  in their Foundry project. The Set up your endpoint page tells them how to
  deploy one if it is missing, and records a check when it answers.
- **Grader changes** only reach students through a Codio publish. Bump the
  guide version line on the Overview page with every grader change so the
  assignment has a visible change to publish.
- **Catalog drift.** The Part 1 questions were written against durable facts,
  but the catalog evolves; give the quiz a quick pass each term.
