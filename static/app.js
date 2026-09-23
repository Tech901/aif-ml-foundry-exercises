// Front-end logic for the Foundry Prompt Lab test bed.
// Loads the challenge from the Flask back end, keeps the student's prompt saved on the
// server as they type, and shows each Run as a card, newest on top. Grading happens in
// the guide's Check button, not here.

const bannerEl = document.getElementById("config-banner");
const statusEl = document.getElementById("status");
const runBtn = document.getElementById("run-btn");
const logEl = document.getElementById("log");

const systemEditor = document.getElementById("editor-system");
const systemInput = document.getElementById("system-prompt");
const userEditor = document.getElementById("editor-user");
const userInput = document.getElementById("user-prompt");
const fixedSystemBox = document.getElementById("fixed-system");
const fixedTestsBox = document.getElementById("fixed-tests");

let challenges = [];
let current = null;
let saveTimer = null;
let runCount = 0;

// --- Small helpers -----------------------------------------------------------

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function setList(id, items) {
  const list = document.getElementById(id);
  list.innerHTML = "";
  for (const item of items) list.appendChild(el("li", "", item));
}

function setBusy(busy) {
  runBtn.disabled = busy;
  statusEl.textContent = busy ? "Sending your prompt to memphis-copilot..." : "";
}

// --- The brief ---------------------------------------------------------------

function selectChallenge(id) {
  current = challenges.find((c) => c.id === id) || challenges[0];

  document.getElementById("challenge-title").textContent = `Challenge ${current.id} — ${current.title}`;
  document.getElementById("challenge-goal").textContent = current.goal;
  document.getElementById("challenge-scenario").textContent = current.scenario;
  setList("requirements", current.requirements);

  const rubricEl = document.getElementById("rubric");
  rubricEl.innerHTML = "";
  for (const item of current.rubric) {
    const li = el("li");
    li.appendChild(el("strong", "", `${item.name} (${item.max} pts): `));
    li.appendChild(document.createTextNode(item.description));
    rubricEl.appendChild(li);
  }

  const attachmentBox = document.getElementById("attachment-box");
  const attachments = current.attachments || [];
  if (attachments.length) {
    document.getElementById("attachment-label").textContent = current.attachment_label || "Provided text";
    const listEl = document.getElementById("attachment-list");
    listEl.innerHTML = "";
    for (const attachment of attachments) {
      if (attachment.label) listEl.appendChild(el("div", "attachment-name", attachment.label));
      const pre = document.createElement("pre");
      pre.textContent = attachment.text;
      listEl.appendChild(pre);
    }
    attachmentBox.classList.remove("hidden");
  } else {
    attachmentBox.classList.add("hidden");
  }

  const writesSystem = current.write.includes("system");
  const writesUser = current.write.includes("user");
  systemEditor.classList.toggle("hidden", !writesSystem);
  userEditor.classList.toggle("hidden", !writesUser);

  if (!writesSystem && current.fixed_system_prompt) {
    document.getElementById("fixed-system-text").textContent = current.fixed_system_prompt;
    fixedSystemBox.classList.remove("hidden");
  } else {
    fixedSystemBox.classList.add("hidden");
  }
  if (!writesUser && current.test_messages) {
    const list = document.getElementById("fixed-tests-list");
    list.innerHTML = "";
    for (const message of current.test_messages) list.appendChild(el("li", "", message));
    fixedTestsBox.classList.remove("hidden");
  } else {
    fixedTestsBox.classList.add("hidden");
  }

  userInput.placeholder = current.weak_prompt
    ? `Improve on: "${current.weak_prompt}"`
    : "Type the message you want to send to the model...";
  document.getElementById("user-hint").textContent = current.starter_user_prompt
    ? "a starter is provided - the system prompt should do the real work"
    : "the message you send to the model";

  logEl.innerHTML = "";
  statusEl.textContent = "";
}

// --- Saving: the server file is what the Check button grades -----------------

async function loadSaved() {
  try {
    const saved = await (await fetch(`/api/prompts/${current.id}`)).json();
    systemInput.value = saved.system || "";
    userInput.value = saved.user || current.starter_user_prompt || "";
  } catch (err) {
    userInput.value = current.starter_user_prompt || "";
  }
}

async function saveNow() {
  if (!current) return;
  try {
    await fetch(`/api/prompts/${current.id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ system_prompt: systemInput.value, user_prompt: userInput.value }),
    });
  } catch (err) {
    /* the next Run saves too */
  }
}

function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, 600);
}

systemInput.addEventListener("input", scheduleSave);
userInput.addEventListener("input", scheduleSave);
systemInput.addEventListener("blur", saveNow);
userInput.addEventListener("blur", saveNow);

// --- Rendering a run as a card, newest on top ----------------------------------

function formatLines(formatCheck) {
  const rows = [];
  formatCheck.checks.forEach((check, i) => {
    const parts = [];
    parts.push(check.reply_is_valid_json ? "valid JSON" : "NOT valid JSON");
    parts.push(check.reply_is_json_only ? "JSON only" : "extra text or a code fence around it");
    parts.push(check.missing_keys.length === 0 ? "all keys present" : "missing keys: " + check.missing_keys.join(", "));
    if (check.extra_keys.length) parts.push("unexpected keys: " + check.extra_keys.join(", "));
    parts.push((check.blank_fields || []).length === 0 ? "no blank values" : "blank values: " + check.blank_fields.join(", "));
    parts.push((check.invalid_values || []).length === 0 ? "right types and values" : "wrong type or value: " + check.invalid_values.join("; "));
    const clean = check.reply_is_valid_json && check.reply_is_json_only && !check.missing_keys.length
      && !check.extra_keys.length && !(check.blank_fields || []).length && !(check.invalid_values || []).length;
    rows.push({ label: check.label || `Test message ${i + 1}`, text: parts.join("  ·  "), clean });
  });
  return rows;
}

function renderRun(data) {
  runCount += 1;
  const card = el("article", "card");
  const head = el("div", "card-head");
  head.appendChild(el("span", "card-title", `Run ${runCount}`));
  head.appendChild(el("span", "clock", data.elapsed_s ? `${data.elapsed_s}s` : ""));
  card.appendChild(head);

  for (const t of data.transcripts) {
    const convo = el("div", "convo");
    if (t.label) convo.appendChild(el("div", "attachment-name", t.label));
    const userMsg = el("div", "msg user");
    userMsg.appendChild(el("div", "bubble", t.user));
    const botMsg = el("div", "msg assistant");
    botMsg.appendChild(el("div", "bubble", t.assistant));
    convo.appendChild(userMsg);
    convo.appendChild(botMsg);
    card.appendChild(convo);
  }

  if (data.format_check && data.format_check.checks) {
    const fc = el("div", "format-check");
    fc.appendChild(el("div", "format-check-title", "Automatic format check"));
    for (const row of formatLines(data.format_check)) {
      fc.appendChild(el("div", "format-check-row " + (row.clean ? "clean" : "dirty"), row.label + ":  " + row.text));
    }
    card.appendChild(fc);
  }

  card.appendChild(el("p", "hint", "Read the replies against the requirements on the left. Edit the prompt and Run again, or press the Check button on the guide page to have it graded."));
  logEl.prepend(card);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderProblem(message, detail) {
  runCount += 1;
  const card = el("article", "card problem");
  const head = el("div", "card-head");
  head.appendChild(el("span", "card-title", `Run ${runCount}`));
  card.appendChild(head);
  card.appendChild(el("div", "msg-problem", message));
  if (detail) card.appendChild(el("pre", "detail", detail));
  logEl.prepend(card);
}

// --- Running -----------------------------------------------------------------

runBtn.addEventListener("click", async () => {
  if (!current) return;
  clearTimeout(saveTimer);
  setBusy(true);
  try {
    const res = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ challenge_id: current.id, system_prompt: systemInput.value, user_prompt: userInput.value }),
    });
    const data = await res.json();
    if (!res.ok) {
      renderProblem(data.error || "Something went wrong.", data.detail);
      return;
    }
    renderRun(data);
  } catch (err) {
    renderProblem("Could not reach the test bed: " + err.message + ". Is it still running? The guide's start page has a link that restarts it.");
  } finally {
    setBusy(false);
  }
});

// --- Boot --------------------------------------------------------------------

async function refreshHealth() {
  try {
    const health = await (await fetch("/api/health")).json();
    if (!health.configured) {
      bannerEl.textContent = "Not configured yet: " + health.missing.join(", ")
        + ". Fill in .env on the Set up your endpoint page and save; no restart is needed.";
      bannerEl.classList.remove("hidden");
    } else {
      bannerEl.classList.add("hidden");
    }
  } catch (err) {
    bannerEl.textContent = "The test bed did not answer. Is it still running?";
    bannerEl.classList.remove("hidden");
  }
}

async function boot() {
  try {
    const challengeData = await (await fetch("/api/challenges")).json();
    challenges = challengeData.challenges;
    selectChallenge(Number(window.CHALLENGE_ID) || challenges[0].id);
    await loadSaved();
  } catch (err) {
    bannerEl.textContent = "Could not load the challenges: " + err.message;
    bannerEl.classList.remove("hidden");
  }
  refreshHealth();
  setInterval(refreshHealth, 5000);
}

boot();
