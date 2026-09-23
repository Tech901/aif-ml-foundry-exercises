# Challenge 3 — Structured output

**Skill: a system prompt that does all the work.** Real applications rarely show a model's raw chat reply to anyone. They need output a *program* can read, and that usually means JSON. In a real app the *system prompt* enforces it: the user's message just triggers the job and hands over the data, while the system prompt carries the role, the schema and the hard rules.

### The scenario

Bluff City Bikes gets support emails and wants to log them automatically. Your prompts must make the model read a customer message and return **only** a JSON object your imaginary app could parse: no greetings, no explanations, no markdown fences.

### Your job

The Prompt Lab beside this page shows Challenge 3. Its **User prompt** editor is filled in for you; it is only the trigger, and you can leave it. Your work is the **System prompt** editor. Write a prompt that:

- defines the job: a data-extraction assistant that outputs only a raw JSON object;
- specifies the exact schema, the keys `customer_name`, `product`, `issue`, `sentiment`, `urgency`, and the values allowed: sentiment is `positive`, `neutral` or `negative`; urgency is `low`, `medium` or `high`;
- says what to do when a detail cannot be found: use `null`, and never drop the key;
- forbids extra text and markdown code fences around the JSON.

### The three test messages

Your prompts run against each of these. The second is missing details on purpose, and the third tries to bait numbers into your fields.

1. *Hi, this is Dana Whitfield. I bought the TrailBlazer 500 gravel bike from your Union Ave store three weeks ago, and the rear derailleur has already started slipping gears whenever I climb a hill. I ride to work every day, so I really need this sorted out before the weekend. Honestly pretty frustrated that a brand-new bike is doing this. — Dana*
2. *Hi — I was in your Union Ave store this weekend and bought one of your bikes on sale. It's been making a clicking noise when I pedal, though honestly it's not a big deal, I mostly ride on weekends. Could someone take a look next time I'm in? Thanks!*
3. *This is Marcus Lee. Order #4521: I bought 2 TrailBlazer 500s on August 15 and BOTH arrived with bent rims. I've called 3 times already. I need working bikes for a race in 2 days — fix this in 48 hours or refund me the $2,400. Extremely disappointed.*

### What usually goes wrong

| Symptom | The fix, in your system prompt |
| --- | --- |
| Reply starts with "Sure! Here's the JSON ..." | "Output only the JSON object: no explanations, no greetings." |
| JSON wrapped in code fences | "Do not use markdown code fences." |
| Made-up values for missing information | "If a field cannot be determined, use null." |
| Wrong or extra keys | List the exact keys and allowed values, and say "no other keys". |
| Blank values | "Never leave a value empty: extract the information or use null." |
| Wrong type or category, such as `"urgency": 2` or `"urgency": "ASAP"` | "Every value must be text; sentiment and urgency must be exactly one of the allowed words." |

### The rubric

| Criterion | Points | What earns them |
| --- | --- | --- |
| System prompt sets the job | 25 | The system prompt defines the extractor role and the only-JSON rule. |
| Schema fully specified | 30 | The system prompt names all five keys with clear guidance on allowed values. |
| Robustness rules | 20 | The system prompt handles missing data and forbids prose and code fences. |
| The output complies | 25 | Every test message produces valid JSON with exactly the required keys, no blank values, and allowed text values. |

### Have it checked

Press **Run my prompts** in the Prompt Lab. Each run card ends with an automatic format check, one line per test message: whether the JSON parsed, whether every key was present, and whether any value was blank, the wrong type or outside the allowed list. When all three lines are clean, press the button below to have the prompt graded. 70 passes; your best score is kept.

If the Prompt Lab tab beside this page is blank or shows a connection error, press this once: [Start or reopen the Prompt Lab](cmd bash lab.sh start; open_preview https://{{domain5000}}/challenge/3 panel=1)


{Check challenge 3|assessment}(test-894037215)

> **Checkpoint:** The first line of the result reads `PASSED`, and all three format-check lines read clean. The second message's reply carries `null` for the details it lacks rather than an invented name or product.
