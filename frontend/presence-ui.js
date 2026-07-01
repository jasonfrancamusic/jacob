let jacobVoiceEnabled = localStorage.getItem("jacob_voice_enabled") === "true";

function presenceGreeting() {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) return "Bom dia, Jason.";
  if (hour >= 12 && hour < 18) return "Boa tarde, Jason.";
  return "Boa noite, Jason.";
}

function unlockJacobVoice() {
  if (!("speechSynthesis" in window)) return false;
  window.speechSynthesis.cancel();
  const test = new SpeechSynthesisUtterance(" ");
  test.lang = "pt-BR";
  test.volume = 0;
  window.speechSynthesis.speak(test);
  return true;
}

function pickPortugueseVoice() {
  if (!("speechSynthesis" in window)) return null;
  const voices = window.speechSynthesis.getVoices();
  return voices.find((voice) => voice.lang?.toLowerCase().startsWith("pt-br"))
    || voices.find((voice) => voice.lang?.toLowerCase().startsWith("pt"))
    || voices[0]
    || null;
}

function speakJacob(text, force = false) {
  if ((!jacobVoiceEnabled && !force) || !("speechSynthesis" in window)) return false;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  const voice = pickPortugueseVoice();
  if (voice) utterance.voice = voice;
  utterance.lang = voice?.lang || "pt-BR";
  utterance.rate = 0.92;
  utterance.pitch = 0.9;
  utterance.volume = 1;
  window.speechSynthesis.speak(utterance);
  return true;
}

function loadAssetOnce(type, url) {
  const selector = type === "css" ? `link[href="${url}"]` : `script[src="${url}"]`;
  if (document.querySelector(selector)) return;
  if (type === "css") {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = url;
    document.head.appendChild(link);
  } else {
    const script = document.createElement("script");
    script.src = url;
    document.body.appendChild(script);
  }
}

function loadExtraModules() {
  loadAssetOnce("css", "premium-polish.css");
  loadAssetOnce("css", "development-mode.css");
  loadAssetOnce("js", "development-mode.js");
  loadAssetOnce("css", "conversation-history.css");
  loadAssetOnce("js", "conversation-history.js");
  loadAssetOnce("css", "voice-engine.css");
  loadAssetOnce("js", "voice-engine.js");
}

function createPresenceControls() {
  const controls = document.createElement("div");
  controls.className = "presence-controls";
  controls.innerHTML = `
    <button id="presence-replay" type="button">Repetir presença</button>
    <button id="voice-test" type="button">Testar voz</button>
    <button id="voice-toggle" type="button">Voz: ${jacobVoiceEnabled ? "Ligada" : "Desligada"}</button>
  `;
  document.body.appendChild(controls);

  const voiceButton = document.querySelector("#voice-toggle");
  const testButton = document.querySelector("#voice-test");

  voiceButton?.classList.toggle("active", jacobVoiceEnabled);
  voiceButton?.addEventListener("click", () => {
    unlockJacobVoice();
    jacobVoiceEnabled = !jacobVoiceEnabled;
    localStorage.setItem("jacob_voice_enabled", String(jacobVoiceEnabled));
    voiceButton.textContent = `Voz: ${jacobVoiceEnabled ? "Ligada" : "Desligada"}`;
    voiceButton.classList.toggle("active", jacobVoiceEnabled);
    if (jacobVoiceEnabled) speakJacob("Voz do Jacob ativada. Se você está ouvindo esta frase, a voz está funcionando.", true);
  });

  testButton?.addEventListener("click", () => {
    unlockJacobVoice();
    jacobVoiceEnabled = true;
    localStorage.setItem("jacob_voice_enabled", "true");
    if (voiceButton) {
      voiceButton.textContent = "Voz: Ligada";
      voiceButton.classList.add("active");
    }
    speakJacob("Teste de voz do Jacob. Estou falando pelo navegador agora.", true);
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
  const sequence = [greeting, "Ambiente premium pronto.", "Voice Engine em modo de teste.", "Use o botão Testar voz para liberar o áudio."];

  ritual.classList.remove("hidden");

  for (const text of sequence) {
    if (line) line.textContent = text;
    speakJacob(text);
    await new Promise((resolve) => setTimeout(resolve, 1200));
  }

  ritual.classList.add("hidden");
  sessionStorage.setItem("jacob_presence_shown", "true");

  if (typeof addMessage === "function") {
    addMessage("Jacob", `${greeting} Voice Engine em modo de teste. Clique em Testar voz para confirmar o áudio.`, "jacob");
  }
}

if ("speechSynthesis" in window) {
  window.speechSynthesis.onvoiceschanged = pickPortugueseVoice;
}

loadExtraModules();
createPresenceControls();
createPresenceRitual();
setTimeout(() => runPresenceRitual(false), 500);
