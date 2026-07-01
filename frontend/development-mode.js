const DEV_MODULES = ["Frontend", "Core API", "Brain", "Gateway", "Planner", "Memory", "Timeline", "Guardian", "Presence"];
const DEV_ENDPOINTS = ["/health", "/chat", "/briefing", "/memories", "/guardian", "/timeline"];

function ensureDevelopmentPage() {
  let page = document.querySelector("#page-development");
  if (!page) {
    page = document.createElement("section");
    page.className = "page";
    page.id = "page-development";
    page.innerHTML = `
      <article class="card full-page-card">
        <p class="card-label">Development Mode</p>
        <h2>Jacob desenvolvendo o próprio Jacob</h2>
        <p>Área para acompanhar evolução técnica, módulos ativos e próximos gargalos.</p>
        <div class="dev-grid">
          <div class="dev-stat"><span>Sprint atual</span><strong>005</strong></div>
          <div class="dev-stat"><span>Módulos</span><strong>${DEV_MODULES.length}</strong></div>
          <div class="dev-stat"><span>Endpoints</span><strong>${DEV_ENDPOINTS.length}</strong></div>
          <div class="dev-stat"><span>Fase</span><strong>v0.2</strong></div>
        </div>
        <div class="dev-section">
          <section class="dev-list"><h3>Módulos ativos</h3><div id="dev-modules"></div></section>
          <section class="dev-list"><h3>Endpoints</h3><div id="dev-endpoints"></div></section>
          <section class="dev-list"><h3>Próximos gargalos</h3><ul><li>Histórico de conversa contínuo.</li><li>Persistência mais robusta.</li><li>Integrações reais.</li><li>Refinamento visual premium.</li></ul></section>
          <section class="dev-list"><h3>Regra estratégica</h3><p>Menos telas soltas. Mais capacidades consistentes.</p></section>
        </div>
      </article>`;
    document.querySelector(".main-panel")?.appendChild(page);
  }
  ensureDevelopmentButton();
  renderDevelopmentMode();
}

function ensureDevelopmentButton() {
  if (document.querySelector('[data-page="development"]')) return;
  const button = document.createElement("button");
  button.className = "nav-item";
  button.dataset.page = "development";
  button.innerHTML = "⌘ <span>Dev Mode</span>";
  const nav = document.querySelector(".nav-menu");
  const settingsButton = document.querySelector('[data-page="settings"]');
  nav?.insertBefore(button, settingsButton || null);
  button.addEventListener("click", setDevelopmentPage);
}

function setDevelopmentPage() {
  document.querySelectorAll(".page").forEach((page) => page.classList.remove("active"));
  document.querySelector("#page-development")?.classList.add("active");
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.page === "development"));
  renderDevelopmentMode();
}

function renderDevelopmentMode() {
  const modules = document.querySelector("#dev-modules");
  const endpoints = document.querySelector("#dev-endpoints");
  if (modules) modules.innerHTML = DEV_MODULES.map((item) => `<span class="dev-pill">● ${item}</span>`).join("");
  if (endpoints) endpoints.innerHTML = DEV_ENDPOINTS.map((item) => `<span class="dev-pill">↔ ${item}</span>`).join("");
}

ensureDevelopmentPage();
