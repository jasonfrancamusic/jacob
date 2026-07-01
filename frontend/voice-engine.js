let jacobRecognition = null;
let jacobListening = false;

function createVoicePanel() {
  if (document.querySelector("#voice-panel")) return;
  const panel = document.createElement("div");
  panel.id = "voice-panel";
  panel.className = "voice-panel";
  panel.innerHTML = `
    <div class="voice-pulse"></div>
    <button id="voice-talk" type="button">🎤 Conversar</button>
    <span id="voice-status">Voice Engine pronto</span>
  `;

  const chatForm = document.querySelector("#chat-form");
  const conversationPanel = document.querySelector("#conversation");
  if (chatForm?.parentNode) {
    chatForm.parentNode.insertBefore(panel, chatForm.nextSibling);
  } else if (conversationPanel) {
    conversationPanel.appendChild(panel);
  } else {
    document.body.appendChild(panel);
  }

  document.querySelector("#voice-talk")?.addEventListener("click", toggleVoiceRecognition);
}

function setVoiceStatus(text, listening = false) {
  const panel = document.querySelector("#voice-panel");
  const button = document.querySelector("#voice-talk");
  const status = document.querySelector("#voice-status");
  if (status) status.textContent = text;
  panel?.classList.toggle("listening", listening);
  button?.classList.toggle("listening", listening);
  if (button) button.textContent = listening ? "Estou ouvindo..." : "🎤 Conversar";
}

function setupRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    setVoiceStatus("Voz não suportada neste navegador");
    return null;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "pt-BR";
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    jacobListening = true;
    setVoiceStatus("Estou ouvindo...", true);
  };

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      transcript += event.results[i][0].transcript;
    }
    setVoiceStatus(transcript || "Ouvindo...", true);

    const lastResult = event.results[event.results.length - 1];
    if (lastResult.isFinal) {
      sendVoiceTranscript(transcript.trim());
    }
  };

  recognition.onerror = () => {
    jacobListening = false;
    setVoiceStatus("Não consegui ouvir. Tente novamente.");
  };

  recognition.onend = () => {
    jacobListening = false;
    setVoiceStatus("Voice Engine pronto");
  };

  return recognition;
}

function toggleVoiceRecognition() {
  if (!jacobRecognition) jacobRecognition = setupRecognition();
  if (!jacobRecognition) return;

  if (jacobListening) {
    jacobRecognition.stop();
    return;
  }

  window.speechSynthesis?.cancel();
  jacobRecognition.start();
}

async function sendVoiceTranscript(text) {
  if (!text) return;
  setVoiceStatus("Processando...");
  if (typeof handleMessage === "function") {
    await handleMessage(text);
    setTimeout(() => speakLastJacobMessage(), 500);
  }
}

function speakLastJacobMessage() {
  if (typeof speakJacob !== "function") return;
  const jacobMessages = document.querySelectorAll(".message.jacob p");
  const last = jacobMessages[jacobMessages.length - 1];
  if (last?.textContent) speakJacob(last.textContent);
}

createVoicePanel();
