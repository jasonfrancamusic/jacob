const API_BASE_URL = "http://127.0.0.1:8000";
const CHAT_URL = `${API_BASE_URL}/chat`;
const HEALTH_URL = `${API_BASE_URL}/health`;

const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const quickActions = document.querySelectorAll("[data-prompt]");
const statusPill = document.querySelector("#connection-status");
const connectionText = document.querySelector("#connection-text");
const connectionDetail = document.querySelector("#connection-detail");
const connectionHealth = document.querySelector("#connection-health");

let backendOnline = false;

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
  } catch (error) {
    setConnectionStatus(false);
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

checkBackendHealth();
setInterval(checkBackendHealth, 5000);
