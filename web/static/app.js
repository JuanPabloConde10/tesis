document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tab");
  const panels = document.querySelectorAll(".panel");
  const form = document.getElementById("story-form");
  const characterList = document.getElementById("characters-list");
  const addCharacterButton = document.getElementById("add-character");
  const storyPreview = document.getElementById("story-preview");
  const generateButton = form.querySelector("button.primary");
  const questionsContainer = document.getElementById("questions");
  const scoreValue = document.getElementById("score-value");
  const scoreFill = document.getElementById("score-fill");

  const evaluationQuestions = [
    { key: "coherence", label: "Coherencia de la trama" },
    { key: "characters", label: "Profundidad de los personajes" },
    { key: "pacing", label: "Ritmo narrativo" },
    { key: "tone", label: "Estilo y tono" },
    { key: "surprise", label: "Originalidad y giros" },
  ];

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.target;
      tabs.forEach((btn) => btn.classList.toggle("active", btn === tab));
      panels.forEach((panel) => panel.classList.toggle("active", panel.id === target));
    });
  });

  function addCharacterField(value = "") {
    const row = document.createElement("div");
    row.className = "character-row";

    const input = document.createElement("input");
    input.type = "text";
    input.name = "character";
    input.placeholder = "Nombre y rol del personaje";
    input.value = value;

    const remove = document.createElement("button");
    remove.type = "button";
    remove.textContent = "Quitar";
    remove.addEventListener("click", () => {
      row.remove();
    });

    row.append(input, remove);
    characterList.append(row);
  }

  function getCharacters() {
    const inputs = characterList.querySelectorAll("input[name='character']");
    return Array.from(inputs)
      .map((input) => input.value.trim())
      .filter(Boolean);
  }

  addCharacterButton.addEventListener("click", () => addCharacterField());

  function setLoading(isLoading) {
    generateButton.disabled = isLoading;
    generateButton.textContent = isLoading ? "Generando..." : "Generar cuento";
    storyPreview.classList.toggle("loading", isLoading);
  }

  async function requestStory(payload) {
    const res = await fetch("/api/story", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      const message = data.detail || "No se pudo generar el cuento.";
      throw new Error(message);
    }
    return data.story;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const trama = form.plot.value.trim();
    const genero = form.genre.value.trim();
    const arco = form.arc.value;
    const personajes = getCharacters();

    const payload = { trama, genero, arco, personajes };

    storyPreview.classList.remove("error");
    storyPreview.textContent = "Generando cuento...";
    setLoading(true);

    try {
      const story = await requestStory(payload);
      storyPreview.textContent = story?.trim() || "(Respuesta vacía)";
    } catch (error) {
      storyPreview.textContent = `Error: ${error.message}`;
      storyPreview.classList.add("error");
    } finally {
      setLoading(false);
    }
  });

  function renderQuestions() {
    evaluationQuestions.forEach((question) => {
      const wrapper = document.createElement("div");
      wrapper.className = "question";

      const header = document.createElement("div");
      header.className = "question__header";

      const title = document.createElement("p");
      title.className = "question__title";
      title.textContent = question.label;

      const value = document.createElement("span");
      value.className = "question__value";
      value.textContent = "0";

      header.append(title, value);

      const slider = document.createElement("input");
      slider.type = "range";
      slider.min = "0";
      slider.max = "5";
      slider.step = "1";
      slider.value = "0";
      slider.name = question.key;
      slider.addEventListener("input", () => {
        value.textContent = slider.value;
        updateScore();
      });

      wrapper.append(header, slider);
      questionsContainer.append(wrapper);
    });
  }

  function updateScore() {
    const sliders = questionsContainer.querySelectorAll("input[type='range']");
    if (!sliders.length) return;
    const values = Array.from(sliders).map((slider) => Number(slider.value));
    const total = values.reduce((acc, curr) => acc + curr, 0);
    const average = total / values.length;
    scoreValue.textContent = average.toFixed(1);
    scoreFill.style.width = `${(average / 5) * 100}%`;
  }

  renderQuestions();
  updateScore();
});
