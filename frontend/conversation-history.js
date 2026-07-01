const CONVERSATION_URL = "http://127.0.0.1:8000/conversations";

function setupConversationHistory() {
  const card = document.querySelector("#page-conversation .full-page-card");
  if (!card || document.querySelector("#history-list")) return;
  card.innerHTML = `
    <p class="card-label">Conversa</p>
    <h2>Histórico contínuo</h2>
    <p>Mensagens salvas localmente para continuidade do Jacob.</p>
    <div class="history-actions"><button id="history-refresh" type="button">Atualizar</button><button id="history-clear" type="button">Limpar</button></div>
    <div id="history-list" class="history-list"><p>Carregando...</p></div>`;
  document.querySelector("#history-refresh")?.addEventListener("click", loadConversationHistory);
  document.querySelector("#history-clear")?.addEventListener("click", clearConversationHistory);
}

function renderConversationHistory(messages) {
  const list = document.querySelector("#history-list");
  if (!list) return;
  if (!messages.length) {
    list.innerHTML = "<p>Nenhuma conversa salva ainda.</p>";
    return;
  }
  list.innerHTML = messages.map((m) => {
    const isUser = m.role === "user";
    const author = isUser ? "Jason" : "Jacob";
    const date = new Date(m.created_at).toLocaleString("pt-BR");
    return `<article class="history-message ${isUser ? "user" : "assistant"}"><header><strong>${author}</strong><small>${date}</small></header><p>${m.content}</p></article>`;
  }).join("");
}

async function loadConversationHistory() {
  setupConversationHistory();
  const list = document.querySelector("#history-list");
  try {
    const response = await fetch(CONVERSATION_URL, { cache: "no-store" });
    const payload = await response.json();
    renderConversationHistory(payload.messages || []);
  } catch (error) {
    if (list) list.innerHTML = "<p>Histórico indisponível. Verifique o backend.</p>";
  }
}

async function clearConversationHistory() {
  await fetch(CONVERSATION_URL, { method: "DELETE" });
  await loadConversationHistory();
}

setupConversationHistory();
loadConversationHistory();
