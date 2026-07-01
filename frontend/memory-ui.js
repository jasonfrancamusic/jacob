const MEMORY_URL = "http://127.0.0.1:8000/memories";

function ensureMemoryPage() {
  let page = document.querySelector("#page-memory");
  if (!page) {
    page = document.createElement("section");
    page.className = "page";
    page.id = "page-memory";
    page.innerHTML = `
      <article class="card full-page-card">
        <p class="card-label">Memory Engine 2.0</p>
        <h2>Memórias autorizadas do Jacob</h2>
        <p>Gerencie o que o Jacob pode lembrar. Transparência e controle são parte central do produto.</p>

        <form id="memory-form" class="memory-form">
          <input id="memory-key" type="text" placeholder="Chave: exemplo projeto_atual" required />
          <input id="memory-value" type="text" placeholder="Valor: o que Jacob deve lembrar" required />
          <select id="memory-category">
            <option value="general">Geral</option>
            <option value="projects">Projetos</option>
            <option value="habits">Hábitos</option>
            <option value="long_term">Longo prazo</option>
            <option value="emotional">Emocional</option>
            <option value="spiritual">Espiritual</option>
            <option value="dreams">Sonhos</option>
          </select>
          <button type="submit">Salvar</button>
        </form>

        <p id="memory-status" class="memory-status">Carregando memórias...</p>
        <div id="memory-list" class="memory-list"></div>
      </article>
    `;
    document.querySelector(".main-panel")?.appendChild(page);
  }

  if (!document.querySelector('[data-page="memory"]')) {
    const memoryButton = document.createElement("button");
    memoryButton.className = "nav-item";
    memoryButton.dataset.page = "memory";
    memoryButton.innerHTML = "◇ <span>Memória</span>";
    const nav = document.querySelector(".nav-menu");
    const settingsButton = document.querySelector('[data-page="settings"]');
    nav?.insertBefore(memoryButton, settingsButton || null);
    memoryButton.addEventListener("click", () => {
      setMemoryPage();
    });
  }
}

function setMemoryPage() {
  document.querySelectorAll(".page").forEach((page) => page.classList.remove("active"));
  document.querySelector("#page-memory")?.classList.add("active");
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.page === "memory");
  });
  loadMemories();
}

function renderMemories(memories) {
  const list = document.querySelector("#memory-list");
  const status = document.querySelector("#memory-status");
  if (!list || !status) return;

  status.textContent = `${memories.length} memória(s) autorizada(s).`;

  if (!memories.length) {
    list.innerHTML = `<article class="memory-item"><p>Nenhuma memória salva ainda.</p></article>`;
    return;
  }

  list.innerHTML = memories.map((memory) => `
    <article class="memory-item">
      <header>
        <strong>${memory.key}</strong>
        <small>${memory.category} • importância ${memory.importance}</small>
      </header>
      <p>${memory.value}</p>
      <button type="button" data-delete-memory="${memory.id}">Excluir memória</button>
    </article>
  `).join("");

  document.querySelectorAll("[data-delete-memory]").forEach((button) => {
    button.addEventListener("click", async () => {
      await deleteMemory(button.dataset.deleteMemory);
    });
  });
}

async function loadMemories() {
  const status = document.querySelector("#memory-status");
  try {
    const response = await fetch(MEMORY_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`Memory error: ${response.status}`);
    const memories = await response.json();
    renderMemories(memories);
  } catch (error) {
    if (status) status.textContent = "Não consegui carregar memórias. Verifique se o backend está rodando.";
  }
}

async function createMemory(event) {
  event.preventDefault();
  const status = document.querySelector("#memory-status");
  const key = document.querySelector("#memory-key")?.value.trim();
  const value = document.querySelector("#memory-value")?.value.trim();
  const category = document.querySelector("#memory-category")?.value;

  if (!key || !value || !category) return;

  try {
    const response = await fetch(MEMORY_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, value, category, importance: 3, authorized: true, source: "frontend" }),
    });
    if (!response.ok) throw new Error(`Create memory error: ${response.status}`);
    document.querySelector("#memory-form")?.reset();
    if (status) status.textContent = "Memória salva com sucesso.";
    await loadMemories();
  } catch (error) {
    if (status) status.textContent = "Não consegui salvar a memória agora.";
  }
}

async function deleteMemory(memoryId) {
  const status = document.querySelector("#memory-status");
  try {
    const response = await fetch(`${MEMORY_URL}/${memoryId}`, { method: "DELETE" });
    if (!response.ok) throw new Error(`Delete memory error: ${response.status}`);
    if (status) status.textContent = "Memória excluída.";
    await loadMemories();
  } catch (error) {
    if (status) status.textContent = "Não consegui excluir essa memória agora.";
  }
}

ensureMemoryPage();
loadMemories();

const memoryForm = document.querySelector("#memory-form");
if (memoryForm) memoryForm.addEventListener("submit", createMemory);
