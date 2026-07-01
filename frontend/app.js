const API_BASE_URL = "http://127.0.0.1:8000";
const CHAT_URL = `${API_BASE_URL}/chat`;
const HEALTH_URL = `${API_BASE_URL}/health`;
const BRIEFING_URL = `${API_BASE_URL}/briefing?partner_name=Jason`;

const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const quickActions = document.querySelectorAll("[data-prompt]");
const statusPill = document.querySelector("#connection-status");
const connectionText = document.querySelector("#connection-text");
const connectionDetail = document.querySelector("#connection-detail");
const connectionHealth = document.querySelector("#connection-health");

let backendOnline = false;

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element && value) element.textContent = value;
}

function addMessage(author, text, type) {
  const article = document.createElement("article");
  article.className = `message ${type}`;

  const header = document.createElement("div");
  header.className = "message-header";

  const strong = document.createElement("strong");
  strong.textContent = author;

  const time = document.createElement("span");
  time.textContent = new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });

  const paragraph = document.createElement("p");
  paragraph.textContent = text;

  header.appendChild(strong);
  header.appendChild(time);
  article.appendChild(header);
  article.appendChild(paragraph);
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
}

function setConnectionStatus(isOnline) {
  backendOnline = isOnline;

  if (statusPill) {
    statusPill.textContent = isOnline ? "● Online" : "● Offline";
    statusPill.classList.toggle("offline", !isOnline);
  }

  if (connectionText) connectionText.textContent = isOnline ? "Jacob Core" : "Jacob Core offline";
  if (connectionDetail) {
    connectionDetail.textContent = isOnline
      ? "Todos os sistemas operacionais"
      : "Inicie o backend em http://127.0.0.1:8000";
  }
  if (connectionHealth) connectionHealth.textContent = isOnline ? "100% online" : "Aguardando backend";
}

async function checkBackendHealth() {
  try {
    const response = await fetch(HEALTH_URL, { cache: "no-store" });
    setConnectionStatus(response.ok);
    return response.ok;
  } catch (error) {
    setConnectionStatus(false);
    return false;
  }
}

async function loadBriefing() {
  const isOnline = await checkBackendHealth();
  if (!isOnline) return;

  try {
    const response = await fetch(BRIEFING_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Briefing error: ${response.status}`);
    const briefing = await response.json();

    setText("#hero-title", briefing.greeting);
    setText("#mission-title", briefing.mission_title);
    setText("#mission-description", briefing.mission_description);
    setText("#mission-progress-label", `${briefing.mission_progress}%`);
    setText("#next-action-title", briefing.next_action?.title);
    setText("#next-action-priority", `● Prioridade ${briefing.next_action?.priority || "alta"}`);
    setText("#reminder-text", briefing.reminder);

    const progressBar = document.querySelector("#mission-progress-bar");
    if (progressBar) progressBar.style.width = `${briefing.mission_progress}%`;

    const focusList = document.querySelector("#focus-list");
    if (focusList && Array.isArray(briefing.focus_items)) {
      focusList.innerHTML = briefing.focus_items.map((item) => `<li>${item}</li>`).join("");
    }
  } catch (error) {
    console.error(error);
  }
}

async function sendMessage(message) {
  const response = await fetch(CHAT_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ partner_name: "Jason", message }),
  });

  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

function localFallbackResponse(message) {
  const text = message.toLowerCase();
  if (text.includes("funcionando") || text.includes("online")) {
    return "Ainda não estou conectado ao Jacob Core. Para eu responder de verdade, deixe o backend rodando em http://127.0.0.1:8000.";
  }
  return "Estou em modo visual agora. O painel abriu, mas o Jacob Core API ainda não está conectado. Inicie o backend e eu volto a responder pelo núcleo real.";
}

async function handleMessage(message) {
  if (!message.trim()) return;

  addMessage("Jason", message, "user");
  input.value = "";
  input.disabled = true;
  form.querySelector("button").disabled = true;

  await checkBackendHealth();

  try {
    if (!backendOnline) throw new Error("Backend offline");
    const payload = await sendMessage(message);
    addMessage("Jacob", payload.text, "jacob");
  } catch (error) {
    addMessage("Jacob", localFallbackResponse(message), "jacob");
    console.error(error);
  } finally {
    input.disabled = false;
    form.querySelector("button").disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await handleMessage(input.value.trim());
});

quickActions.forEach((button) => {
  button.addEventListener("click", async () => {
    await handleMessage(button.dataset.prompt);
  });
});

loadBriefing();
setInterval(checkBackendHealth, 5000);
