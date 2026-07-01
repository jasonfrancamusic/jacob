const API_BASE_URL = "http://127.0.0.1:8000";
const CHAT_URL = `${API_BASE_URL}/chat`;
const HEALTH_URL = `${API_BASE_URL}/health`;
const BRIEFING_URL = `${API_BASE_URL}/briefing?partner_name=Jason`;
const GUARDIAN_URL = `${API_BASE_URL}/guardian`;
const TIMELINE_URL = `${API_BASE_URL}/timeline`;

const BOA_VISTA = { latitude: 2.8235, longitude: -60.6758, label: "Boa Vista, RR" };

const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const quickActions = document.querySelectorAll("[data-prompt]");
const statusPill = document.querySelector("#connection-status");
const connectionText = document.querySelector("#connection-text");
const connectionDetail = document.querySelector("#connection-detail");
const connectionHealth = document.querySelector("#connection-health");
const osWindow = document.querySelector(".os-window");

let backendOnline = false;

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element && value !== undefined && value !== null) element.textContent = value;
}

function currentTime() {
  return new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
}

function greetingForHour(hour) {
  if (hour >= 5 && hour < 12) return "Bom dia";
  if (hour >= 12 && hour < 18) return "Boa tarde";
  return "Boa noite";
}

function updateLocalTimeAndGreeting() {
  const now = new Date();
  const greeting = greetingForHour(now.getHours());
  const date = now.toLocaleDateString("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  setText("#greeting-eyebrow", `${greeting}, Jason.`);
  setText("#hero-title", `${greeting}, Jason.`);
  setText("#date-line", date.charAt(0).toUpperCase() + date.slice(1));
  setText("#time-value", `◷ ${currentTime()}`);
}

async function loadWeather() {
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${BOA_VISTA.latitude}&longitude=${BOA_VISTA.longitude}&current=temperature_2m&timezone=America%2FBoa_Vista`;
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error("Weather unavailable");
    const data = await response.json();
    const temp = Math.round(data.current?.temperature_2m);
    if (!Number.isNaN(temp)) setText("#weather-value", `☼ ${temp}°C`);
    setText("#weather-label", BOA_VISTA.label);
  } catch (error) {
    setText("#weather-value", "☼ --°C");
    setText("#weather-label", BOA_VISTA.label);
  }
}

function addMessage(author, text, type) {
  const article = document.createElement("article");
  article.className = `message ${type}`;

  const header = document.createElement("div");
  header.className = "message-header";

  const strong = document.createElement("strong");
  strong.textContent = author;

  const time = document.createElement("span");
  time.textContent = currentTime();

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

  setText("#core-value", isOnline ? "◉ Online" : "◉ Offline");
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

function ensureGuardianPreviewCard() {
  let card = document.querySelector("#guardian-preview-card");
  if (card) return card;

  const missionGrid = document.querySelector(".mission-grid");
  if (!missionGrid) return null;

  card = document.createElement("article");
  card.id = "guardian-preview-card";
  card.className = "card small-card guardian-card";
  card.innerHTML = `
    <p class="card-label">Guardian</p>
    <h3 id="guardian-summary">Guardian aguardando leitura...</h3>
    <ul id="guardian-preview-list"><li>Carregando observações...</li></ul>
  `;
  missionGrid.appendChild(card);
  return card;
}

function ensureTimelinePage() {
  let page = document.querySelector("#page-timeline");
  if (!page) {
    page = document.createElement("section");
    page.className = "page";
    page.id = "page-timeline";
    page.innerHTML = `
      <article class="card full-page-card">
        <p class="card-label">Timeline</p>
        <h2>Linha do tempo do Jacob OS</h2>
        <p>Os marcos importantes do projeto aparecem aqui automaticamente pelo Timeline Engine.</p>
        <div id="timeline-list" class="timeline-list"><p>Carregando timeline...</p></div>
      </article>
    `;
    document.querySelector(".main-panel")?.appendChild(page);
  }

  if (!document.querySelector('[data-page="timeline"]')) {
    const timelineButton = document.createElement("button");
    timelineButton.className = "nav-item";
    timelineButton.dataset.page = "timeline";
    timelineButton.innerHTML = "◷ <span>Timeline</span>";
    const nav = document.querySelector(".nav-menu");
    const lifeButton = document.querySelector('[data-page="life"]');
    nav?.insertBefore(timelineButton, lifeButton || null);
    timelineButton.addEventListener("click", () => setPage("timeline"));
  }
}

function ensureGuardianPage() {
  let page = document.querySelector("#page-guardian");
  if (!page) {
    page = document.createElement("section");
    page.className = "page";
    page.id = "page-guardian";
    page.innerHTML = `
      <article class="card full-page-card">
        <p class="card-label">Guardian</p>
        <h2>Observador silencioso</h2>
        <p>O Guardian prepara observações para o Brain antes de você conversar com Jacob.</p>
        <div id="guardian-list" class="guardian-list"><p>Carregando Guardian...</p></div>
      </article>
    `;
    document.querySelector(".main-panel")?.appendChild(page);
  }

  if (!document.querySelector('[data-page="guardian"]')) {
    const guardianButton = document.createElement("button");
    guardianButton.className = "nav-item";
    guardianButton.dataset.page = "guardian";
    guardianButton.innerHTML = "◆ <span>Guardian</span>";
    const nav = document.querySelector(".nav-menu");
    const settingsButton = document.querySelector('[data-page="settings"]');
    nav?.insertBefore(guardianButton, settingsButton || null);
    guardianButton.addEventListener("click", () => setPage("guardian"));
  }
}

async function loadGuardian() {
  ensureGuardianPreviewCard();
  ensureGuardianPage();

  try {
    const response = await fetch(GUARDIAN_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Guardian error: ${response.status}`);
    const guardian = await response.json();
    const observations = guardian.observations || [];

    setText("#guardian-summary", guardian.summary || "Guardian ativo.");

    const preview = document.querySelector("#guardian-preview-list");
    if (preview) {
      preview.innerHTML = observations.slice(0, 2).map((item) => `<li>${item.title}</li>`).join("") || "<li>Nenhuma observação.</li>";
    }

    const full = document.querySelector("#guardian-list");
    if (full) {
      full.innerHTML = observations.map((item) => `
        <article class="timeline-item">
          <span>${item.category} • ${item.priority}</span>
          <h3>${item.title}</h3>
          <p>${item.description}</p>
        </article>
      `).join("") || "<p>Nenhuma observação disponível.</p>";
    }
  } catch (error) {
    setText("#guardian-summary", "Guardian indisponível. Verifique o backend.");
  }
}

async function loadTimeline() {
  ensureTimelinePage();

  try {
    const response = await fetch(TIMELINE_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Timeline error: ${response.status}`);
    const payload = await response.json();
    const events = payload.events || [];
    const list = document.querySelector("#timeline-list");
    if (!list) return;

    list.innerHTML = events.map((event) => {
      const date = new Date(event.created_at).toLocaleDateString("pt-BR");
      return `
        <article class="timeline-item">
          <span>${date} • ${event.category}</span>
          <h3>${event.title}</h3>
          <p>${event.description}</p>
        </article>
      `;
    }).join("") || "<p>Nenhum evento na timeline ainda.</p>";
  } catch (error) {
    const list = document.querySelector("#timeline-list");
    if (list) list.innerHTML = "<p>Não consegui carregar a timeline. Verifique o backend.</p>";
  }
}

async function loadBriefing() {
  const isOnline = await checkBackendHealth();
  if (!isOnline) return;

  try {
    const response = await fetch(BRIEFING_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Briefing error: ${response.status}`);
    const briefing = await response.json();

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

    if (briefing.guardian) await loadGuardian();
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

function setPage(pageName) {
  document.querySelectorAll(".page").forEach((page) => page.classList.remove("active"));
  document.querySelector(`#page-${pageName}`)?.classList.add("active");

  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.page === pageName);
  });

  if (pageName === "timeline") loadTimeline();
  if (pageName === "guardian") loadGuardian();
}

function setAvatarMode(mode) {
  osWindow.dataset.avatar = mode;
  document.querySelector("#sphere-mode")?.classList.toggle("selected", mode === "sphere");
  document.querySelector("#human-mode")?.classList.toggle("selected", mode === "human");
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

document.querySelectorAll("[data-page]").forEach((button) => {
  button.addEventListener("click", () => setPage(button.dataset.page));
});

document.querySelectorAll("[data-page-jump]").forEach((button) => {
  button.addEventListener("click", () => setPage(button.dataset.pageJump));
});

document.querySelector("#sphere-mode")?.addEventListener("click", () => setAvatarMode("sphere"));
document.querySelector("#human-mode")?.addEventListener("click", () => setAvatarMode("human"));

ensureTimelinePage();
ensureGuardianPage();
updateLocalTimeAndGreeting();
loadWeather();
loadBriefing();
loadTimeline();
loadGuardian();
setInterval(updateLocalTimeAndGreeting, 10000);
setInterval(checkBackendHealth, 5000);
