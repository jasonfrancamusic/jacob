let jacobVoiceEnabled = localStorage.getItem("jacob_voice_enabled") === "true";

function presenceGreeting() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) return "Bom dia, Jason.";
  if (hour >= 12 && hour < 18) return "Boa tarde, Jason.";
  return "Boa noite, Jason.";
}

function speakJacob(text) {
  if (!jacobVoiceEnabled || !("speechSynthesis" in window)) return;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "pt-BR";
  utterance.rate = 0.92;
  utterance.pitch = 0.9;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}

function loadDevelopmentMode() {
  if (!document.querySelector('link[href="development-mode.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "development-mode.css";
    document.head.appendChild(link);
  }

  if (!document.querySelector('script[src="development-mode.js"]')) {
    const script = document.createElement("script");
    script.src = "development-mode.js";
    document.body.appendChild(script);
  }
}

function createPresenceControls() {
  const controls = document.createElement("div");
  controls.className = "presence-controls";
  controls.innerHTML = `
    <button id="presence-replay" type="button">Repetir presença</button>
    <button id="voice-toggle" type="button">Voz: ${jacobVoiceEnabled ? "Ligada" : "Desligada"}</button>
  `;
  document.body.appendChild(controls);

  const voiceButton = document.querySelector("#voice-toggle");
  voiceButton?.classList.toggle("active", jacobVoiceEnabled);
  voiceButton?.addEventListener("click", () => {
    jacobVoiceEnabled = !jacobVoiceEnabled;
    localStorage.setItem("jacob_voice_enabled", String(jacobVoiceEnabled));
    voiceButton.textContent = `Voz: ${jacobVoiceEnabled ? "Ligada" : "Desligada"}`;
    voiceButton.classList.toggle("active", jacobVoiceEnabled);
    if (jacobVoiceEnabled) speakJacob("Voz do Jacob ativada.");
  });

  document.querySelector("#presence-replay")?.addEventListener("click", () => runPresenceRitual(true));
}

function createPresenceRitual() {
  let ritual = document.querySelector("#presence-ritual");
  if (ritual) return ritual;

  ritual = document.createElement("section");
  ritual.id = "presence-ritual";
  ritual.className = "presence-ritual hidden";
  ritual.innerHTML = `
    <div class="presence-box">
      <div class="presence-orb"></div>
      <div id="presence-line" class="presence-line">Inicializando Jacob OS...</div>
    </div>
  `;
  document.body.appendChild(ritual);
  return ritual;
}

async function runPresenceRitual(force = false) {
  const alreadyShown = sessionStorage.getItem("jacob_presence_shown") === "true";
  if (alreadyShown && !force) return;

  const ritual = createPresenceRitual();
  const line = document.querySelector("#presence-line");
  const greeting = presenceGreeting();
  const sequence = [
    greeting,
    "Eu estava preparando o ambiente.",
    "Guardian, Timeline, Memory e Development Mode estão prontos para evoluir.",
    "Vamos continuar de onde paramos."
  ];

  ritual.classList.remove("hidden");

  for (const text of sequence) {
    if (line) line.textContent = text;
    speakJacob(text);
    await new Promise((resolve) => setTimeout(resolve, 1450));
  }

  ritual.classList.add("hidden");
  sessionStorage.setItem("jacob_presence_shown", "true");

  if (typeof addMessage === "function") {
    addMessage("Jacob", `${greeting} Presence Engine 2.0 ativo. Estou aqui e pronto para continuar.`, "jacob");
  }
}

loadDevelopmentMode();
createPresenceControls();
createPresenceRitual();
setTimeout(() => runPresenceRitual(false), 500);
