function getGreetingByHour(hour) {
  if (hour >= 5 && hour < 12) return "Bom dia";
  if (hour >= 12 && hour < 18) return "Boa tarde";
  return "Boa noite";
}

function formatAmbientDate(now) {
  const date = now.toLocaleDateString("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
  return date.charAt(0).toUpperCase() + date.slice(1);
}

function renderAmbientClock() {
  const now = new Date();
  const greeting = getGreetingByHour(now.getHours());
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");

  const title = document.querySelector("#hero-title");
  if (title) title.innerHTML = `${greeting}, <span>Jason.</span>`;

  const dateLine = document.querySelector("#date-line");
  if (dateLine) dateLine.textContent = formatAmbientDate(now);

  const timeValue = document.querySelector("#time-value");
  if (timeValue) {
    timeValue.innerHTML = `<span class="ambient-time"><span class="ambient-time-main">◷ ${hours}:${minutes}</span><span class="ambient-time-seconds">:${seconds}</span></span>`;
  }

  document.body.classList.toggle("ambient-night", now.getHours() >= 18 || now.getHours() < 5);
}

function setAmbientTemperature(temp) {
  const body = document.body;
  body.classList.remove("ambient-cold", "ambient-mild", "ambient-warm", "ambient-hot", "ambient-extreme");

  if (temp <= 18) body.classList.add("ambient-cold");
  else if (temp <= 25) body.classList.add("ambient-mild");
  else if (temp <= 31) body.classList.add("ambient-warm");
  else if (temp <= 36) body.classList.add("ambient-hot");
  else body.classList.add("ambient-extreme");
}

function readCurrentTemperatureFromDom() {
  const weather = document.querySelector("#weather-value")?.textContent || "";
  const match = weather.match(/-?\d+/);
  if (!match) return null;
  return Number(match[0]);
}

function observeWeatherValue() {
  const weather = document.querySelector("#weather-value");
  if (!weather) return;

  const apply = () => {
    const temp = readCurrentTemperatureFromDom();
    if (Number.isFinite(temp)) setAmbientTemperature(temp);
  };

  apply();
  const observer = new MutationObserver(apply);
  observer.observe(weather, { childList: true, characterData: true, subtree: true });
}

renderAmbientClock();
observeWeatherValue();
setInterval(renderAmbientClock, 1000);
