const API_URL = "http://127.0.0.1:8000/chat";

const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");

function addMessage(author, text, type) {
  const article = document.createElement("article");
  article.className = `message ${type}`;

  const strong = document.createElement("strong");
  strong.textContent = author;

  const paragraph = document.createElement("p");
  paragraph.textContent = text;

  article.appendChild(strong);
  article.appendChild(paragraph);
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(message) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      partner_name: "Jason",
      message,
    }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message) return;

  addMessage("Jason", message, "user");
  input.value = "";
  input.disabled = true;
  form.querySelector("button").disabled = true;

  try {
    const payload = await sendMessage(message);
    addMessage("Jacob", payload.text, "jacob");
  } catch (error) {
    addMessage(
      "Jacob",
      "Não consegui acessar o Jacob Core API agora. Verifique se o backend está rodando em http://127.0.0.1:8000.",
      "jacob"
    );
    console.error(error);
  } finally {
    input.disabled = false;
    form.querySelector("button").disabled = false;
    input.focus();
  }
});
