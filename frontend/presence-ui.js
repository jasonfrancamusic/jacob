let jacobVoiceEnabled = localStorage.getItem("jacob_voice_enabled") !== "false";
let currentPremiumAudio = null;
const PREMIUM_VOICE_URL = "http://127.0.0.1:8000/voice/speak";

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

function waitForBrowserSpeech(utterance) {
  return new Promise((resolve) => {
    utterance.onend = resolve;
    utterance.onerror = resolve;
    setTimeout(resolve, Math.max(2500, utterance.text.length * 120));
  });
}

async function speakBrowserFallback(text, force = false) {
  if ((!jacobVoiceEnabled && !force) || !("speechSynthesis" in window)) return false;
  window.speechSynthesis.cancel();
  const prepared = text.replaceAll("Jacob", "Jay-cub").replaceAll("Jason", "Jay-son");
  const utterance = new SpeechSynthesisUtterance(prepared);
  const voice = pickPortugueseVoice();
  if (voice) utterance.voice = voice;
  utterance.lang = voice?.lang || "pt-BR";
  utterance.rate = 0.86;
  utterance.pitch = 0.82;
  utterance.volume = 1;
  window.speechSynthesis.speak(utterance);
  await waitForBrowserSpeech(utterance);
  return true;
}

function waitForAudio(audio) {
  return new Promise((resolve) => {
    audio.onended = resolve;
    audio.onerror = resolve;
    audio.onpause = () => {
      if (audio.currentTime >= audio.duration - 0.15) resolve();
    };
  });
}

async function speakJacob(text, force = false) {
  if (!jacobVoiceEnabled && !force) return false;

  try {
    window.speechSynthesis?.cancel();
    if (currentPremiumAudio) {
      currentPremiumAudio.pause();
      currentPremiumAudio = null;
    }

    const response = await fetch(PREMIUM_VOICE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) throw new Error("premium voice unavailable");
    const payload = await response.json();
    if (!payload.audio_base64) throw new Error("fallback voice response");

    const audio = new Audio(`data:audio/mp3;base64,${payload.audio_base64}`);
    currentPremiumAudio = audio;
    await audio.play();
    await waitForAudio(audio);
    return true;
  } catch (error) {
    return speakBrowserFallback(text, force);
  }
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
  loadAssetOnce("css", "chat-polish.css");
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
    <button id="voice-test" type="button">Testar voz premium</button>
    <button id="voice-toggle" type="button">Voz: ${jacobVoiceEnabled ? "Ligada" : "Desligada"}</button>
  `;
  document.body.appendChild(controls);

  const voiceButton = document.querySelector("#voice-toggle");
  const testButton = document.querySelector("#voice-test");

  voiceButton?.classList.toggle("active", jacobVoiceEnabled);
  voiceButton?.addEventListener("click", async () => {
    unlockJacobVoice();
    jacobVoiceEnabled = !jacobVoiceEnabled;
    localStorage.setItem("jacob_voice_enabled", String(jacobVoiceEnabled));
    voiceButton.textContent = `Voz: ${jacobVoiceEnabled ? "Ligada" : "Desligada"}`;
    voiceButton.classList.toggle("active", jacobVoiceEnabled);
    if (jacobVoiceEnabled) await speakJacob("Voz do Jacob ativada. A partir de agora, vou falar minhas respostas sempre que possível.", true);
  });

  testButton?.addEventListener("click", async () => {
    unlockJacobVoice();
    jacobVoiceEnabled = true;
    localStorage.setItem("jacob_voice_enabled", "true");
    if (voiceButton) {
      voiceButton.textContent = "Voz: Ligada";
      voiceButton.classList.add("active");
    }
    await speakJacob("Boa noite, Jason. Aqui é o Jacob. Teste de voz premium concluído.", true);
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
    "Voice Identity está em modo premium.",
    "Agora vou esperar cada fala terminar antes de avançar.",
    "Se você quiser usar a voz Will, coloque o Voice ID dela no arquivo de configuração."
  ];

  ritual.classList.remove("hidden");

  for (const text of sequence) {
    if (line) line.textContent = text;
    await speakJacob(text);
    await new Promise((resolve) => setTimeout(resolve, 350));
  }

  ritual.classList.add("hidden");
  sessionStorage.setItem("jacob_presence_shown", "true");

  if (typeof addMessage === "function") {
    addMessage("Jacob", `${greeting} Voz configurada para falar sempre que possível.`, "jacob");
  }
}

if ("speechSynthesis" in window) {
  window.speechSynthesis.onvoiceschanged = pickPortugueseVoice;
}

localStorage.setItem("jacob_voice_enabled", String(jacobVoiceEnabled));
loadExtraModules();
createPresenceControls();
createPresenceRitual();
setTimeout(() => runPresenceRitual(false), 500);
