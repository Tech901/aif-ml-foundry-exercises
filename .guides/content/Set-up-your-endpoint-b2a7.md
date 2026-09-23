# Set up your endpoint

Part 2 sends every prompt to a deployment in **your** Foundry project, so before anything else the code needs two values from you: the **endpoint**, the HTTPS address requests go to, and the **key**, the secret string that proves a request is allowed to use it. Both go in the `.env` file open beside this page, where a small terminal is also installing the Prompt Lab's libraries while you work; leave it alone. The deployment's name, `memphis-copilot`, is already in the code.

### 1. Check the deployment

In the portal, open your project and select **Build → Deployments**. If a row named `memphis-copilot` is there with status Succeeded, go on to item 2. If it is not, deploy it now: **Discover → Models**, search for `gpt-4.1-mini` (not `gpt-4.1-nano`, which sits beside it), **Deploy → Custom settings**, and set these values:

| Field | Value |
| --- | --- |
| Deployment name | `memphis-copilot` |
| Deployment type | Global Standard |
| Tokens per Minute Rate Limit | `100000` |

Leave everything else as the panel proposes and select **Deploy**. The name is the city's choice and says nothing about the model behind it; that is deliberate, because the code sends the deployment's name, never the model's.

### 2. Copy the endpoint and key

Select the round button at the left of the `memphis-copilot` row, not its name, which opens the playground. A detail panel opens on the right holding the endpoint and the key. Each sits in a box with a copy icon at its right end, and those two icons are where your values come from. The pictures on this page are only illustrations.

![The detail panel for a deployment: its version and Succeeded status, the Open in playground, Edit and Delete buttons, then the Project endpoint field with a copy icon and the key field shown as dots with a copy icon; the key value is never displayed](.guides/img/portal-20260901-endpoint-and-keys.png)

Press the copy icon beside **Project endpoint** and paste the value after `AI901_ENDPOINT=` in `.env`. It is longer than the address the code needs: it ends with `/api/projects/` and your project's name. Delete that ending and keep the slash in front of it, as the picture shows.

![Two addresses. The first, labelled what the panel shows, is the host address ending in a slash followed by api/projects/ and a project name, with the api/projects part struck through in red. The second, labelled what goes in the file, is the host address ending in a slash and nothing more.](.guides/img/endpoint-trim.png)

Press the copy icon beside the key and paste the value after `AI901_KEY=`. No spaces around either `=`, no quote marks. Finished, the file has this shape, with your own values in place of the examples:

![The finished .env file: line 1 reads AI901_ENDPOINT= followed by the host address ending in a slash; line 2 reads AI901_KEY= followed by a long key; a comment says to use your own values, one slash at the end of the endpoint, no spaces, no quotes.](.guides/img/env-finished.png)

### 3. Have it checked

The check reads your `.env` and sends one short question to `memphis-copilot`. It passes when the deployment answers, which proves the endpoint, the key and the deployment name at once. Unlimited attempts; your best score counts.

{Check the endpoint and key|assessment}(test-402911736)

> **Checkpoint:** The first line of the result reads `PASSED`. If it reads `NOT YET`, the line under it names the likely cause: a key copied short, an address that still carries `/api/projects/...` or lost its ending slash, or no deployment named `memphis-copilot` in your project. Do not move on until it passes; everything in Part 2 depends on it.

> **Pro Tip:** The key is a secret and `.env` is the only place it goes. It never goes in a prompt, never in a message, never in a screenshot. Anyone holding it can spend against your subscription. If you think you have shown it to somebody, tell your instructor; a key can be replaced in the portal, and the old one stops working.
