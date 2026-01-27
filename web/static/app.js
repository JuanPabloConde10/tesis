document.addEventListener("DOMContentLoaded", () => {
  console.log("=== SCRIPT CARGADO ===");
  const state = {
    aois: { list: [], strategies: [] },
    config: { modes: [], models: [], defaultMode: "", defaultModel: "", aoiNames: [], strategies: [], generationMethods: [] },
    entry: null,
    experiments: [],
    experimentIndex: 0,
    currentExperiment: null,
  };

  const tabs = document.querySelectorAll(".tab");
  const panels = document.querySelectorAll(".panel");
  const tabsContainer = document.querySelector(".tabs");
  const landingPanel = document.getElementById("landing-panel");
  const form = document.getElementById("story-form");
  const characterList = document.getElementById("characters-list");
  const addCharacterButton = document.getElementById("add-character");
  const storyPreview = document.getElementById("story-preview");
  const plotSchemaPanel = document.getElementById("plot-schema-panel");
  const plotSchemaPreview = document.getElementById("plot-schema-preview");
  const generateButton = form.querySelector("button.primary");
  const questionsContainer = document.getElementById("questions");
  const scoreValue = document.getElementById("score-value");
  const scoreFill = document.getElementById("score-fill");
  const startCustom = document.getElementById("start-custom");
  const startExperiments = document.getElementById("start-experiments");
  const resetFlowButton = document.getElementById("reset-flow");
  const modePill = document.getElementById("mode-pill");
  const modelSelect = document.getElementById("model");
  const modeSelect = document.getElementById("mode");
  const modeDescription = document.getElementById("mode-description");
  const modeHint = document.getElementById("mode-hint");
  const aoiOptions = document.getElementById("aoi-options");
  const generationMethodSelect = document.getElementById("generation-method");
  const experimentBanner = document.getElementById("experiment-banner");
  const experimentTitle = document.getElementById("experiment-title");
  const nextExperimentButton = document.getElementById("next-experiment");
  const mode3Fields = document.getElementById("mode3-fields");
  const aoisList = document.getElementById("aois-list");
  const strategySelect = document.getElementById("strategy");
  const mode4Fields = document.getElementById("mode4-fields");
  const mode4AoisList = document.getElementById("mode4-aois-list");
  const mode4StrategySelect = document.getElementById("mode4-strategy");
  const mode4CharactersSection = document.getElementById("mode4-characters-section");
  const mode4CharactersList = document.getElementById("mode4-characters-list");
  const addMode4CharacterButton = document.getElementById("add-mode4-character");


  const evaluationQuestions = [
    { key: "coherence", label: "Coherencia de la trama" },
    { key: "characters", label: "Profundidad de los personajes" },
    { key: "pacing", label: "Ritmo narrativo" },
    { key: "tone", label: "Estilo y tono" },
    { key: "surprise", label: "Originalidad y giros" },
  ];

  function setActivePanel(targetId) {
    panels.forEach((panel) => panel.classList.toggle("active", panel.id === targetId));
    tabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.target === targetId));
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      if (tabsContainer.classList.contains("is-hidden")) return;
      const target = tab.dataset.target;
      setActivePanel(target);
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

  function getSelectedAois() {
    if (!aoiOptions) return [];
    const inputs = aoiOptions.querySelectorAll("input[type='checkbox']");
    return Array.from(inputs)
      .filter((input) => input.checked)
      .map((input) => input.value);
  }

  addCharacterButton.addEventListener("click", () => addCharacterField());

  // Modo 4: Agregar personaje con atributos
  function addMode4Character() {
    const characterCard = document.createElement("div");
    characterCard.className = "character-with-attributes";
    
    const characterIndex = mode4CharactersList.children.length;
    
    characterCard.innerHTML = `
      <input 
        type="text" 
        name="mode4-character-name" 
        placeholder="Nombre del personaje" 
        required
      />
      <input
        type="text"
        name="mode4-character-description"
        placeholder="Descripción (opcional)"
      />
      <div class="character-attributes-grid">
        <div class="attribute-input">
          <label>Valentía</label>
          <input type="number" name="valentia" min="1" max="5" value="3" required />
        </div>
        <div class="attribute-input">
          <label>Bondad</label>
          <input type="number" name="bondad" min="1" max="5" value="3" required />
        </div>
        <div class="attribute-input">
          <label>Astucia</label>
          <input type="number" name="astucia" min="1" max="5" value="3" required />
        </div>
        <div class="attribute-input">
          <label>Maldad</label>
          <input type="number" name="maldad" min="1" max="5" value="3" required />
        </div>
        <div class="attribute-input">
          <label>Carisma</label>
          <input type="number" name="carisma" min="1" max="5" value="3" required />
        </div>
      </div>
      <button type="button" class="remove-character-btn">Eliminar personaje</button>
    `;
    
    // Add remove handler
    const removeBtn = characterCard.querySelector(".remove-character-btn");
    removeBtn.addEventListener("click", () => {
      characterCard.remove();
    });
    
    mode4CharactersList.appendChild(characterCard);
  }

  // Modo 4: Obtener personajes con atributos
  function getMode4Characters() {
    const characterCards = mode4CharactersList.querySelectorAll(".character-with-attributes");
    const characters = [];
    
    characterCards.forEach(card => {
      const nameInput = card.querySelector("input[name='mode4-character-name']");
      const descriptionInput = card.querySelector("input[name='mode4-character-description']");
      const valentia = card.querySelector("input[name='valentia']");
      const bondad = card.querySelector("input[name='bondad']");
      const astucia = card.querySelector("input[name='astucia']");
      const maldad = card.querySelector("input[name='maldad']");
      const carisma = card.querySelector("input[name='carisma']");
      
      const name = nameInput.value.trim();
      const description = descriptionInput.value.trim();
      if (name) {
        characters.push({
          name: name,
          description: description || undefined,
          attributes: {
            valentia: parseInt(valentia.value),
            bondad: parseInt(bondad.value),
            astucia: parseInt(astucia.value),
            maldad: parseInt(maldad.value),
            carisma: parseInt(carisma.value)
          }
        });
      }
    });
    
    return characters;
  }

  if (addMode4CharacterButton) {
    addMode4CharacterButton.addEventListener("click", addMode4Character);
  }

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
    return data;
  }

  function updateModeDescription() {
    const modeId = modeSelect.value;
    const mode = state.config.modes.find((item) => item.id === modeId);
    if (mode) {
      modeDescription.textContent = mode.description || "Modo sin descripción detallada.";
      modeHint.textContent = mode.defaultModel
        ? `Sugerencia: usa ${mode.defaultModel} o cambia aquí mismo.`
        : "Los modos se definen en el backend.";
    } else {
      modeDescription.textContent = "Seleccioná un modo para ver su detalle.";
      modeHint.textContent = "Los modos se definen en el backend.";
    }
  }

  function hydrateModeOptions() {
    modeSelect.innerHTML = '<option value="">Elegí un modo</option>';
    state.config.modes.forEach((mode) => {
      const option = document.createElement("option");
      option.value = mode.id;
      option.textContent = mode.name;
      modeSelect.append(option);
    });
  }

  function hydrateModelOptions() {
    modelSelect.innerHTML = '<option value="">Usar modelo por defecto</option>';
    state.config.models.forEach((model) => {
      const option = document.createElement("option");
      option.value = model;
      option.textContent = model;
      modelSelect.append(option);
    });
  }

  function hydrateAoiOptions() {
    if (!aoiOptions) return;
    aoiOptions.innerHTML = "";
    const aoiNames = state.config.aoiNames || [];
    if (!aoiNames.length) {
      aoiOptions.textContent = "No hay AOIs disponibles.";
      aoiOptions.classList.add("is-empty");
      return;
    }
    aoiOptions.classList.remove("is-empty");
    aoiNames.forEach((name) => {
      const label = document.createElement("label");
      label.className = "aoi-option";

      const input = document.createElement("input");
      input.type = "checkbox";
      input.name = "aoi_names";
      input.value = name;

      const text = document.createElement("span");
      text.textContent = name;

      label.append(input, text);
      aoiOptions.append(label);
    });
  }

  function hydrateGenerationMethodOptions() {
    if (!generationMethodSelect) return;
    generationMethodSelect.innerHTML = '<option value="">Elegí un método</option>';
    (state.config.generationMethods || []).forEach((m) => {
      const opt = document.createElement("option");
      opt.value = m.id;
      opt.textContent = m.name;
      opt.title = m.description;
      generationMethodSelect.append(opt);
    });
  }

  function applyDefaults() {
    if (state.config.defaultMode) {
      modeSelect.value = state.config.defaultMode;
    }
    if (state.config.defaultModel) {
      modelSelect.value = state.config.defaultModel;
    }
    if (generationMethodSelect) generationMethodSelect.value = "";
    updateModeDescription();
  }

  let optionsPromise;

  function ensureOptions() {
    if (!optionsPromise) {
      optionsPromise = loadOptions();
    }
    return optionsPromise;
  }

  async function loadOptions() {
    try {
      const res = await fetch("/api/options");
      const data = await res.json();
      state.config = {
        modes: data.modes || [],
        models: data.models || [],
        defaultMode: data.defaultMode || "",
        defaultModel: data.defaultModel || "",
        aoiNames: data.aoiNames || [],
        strategies: data.strategies || [],
        generationMethods: data.generationMethods || [],
      };
      hydrateModeOptions();
      hydrateModelOptions();
      hydrateAoiOptions();
      hydrateGenerationMethodOptions();
      applyDefaults();
    } catch (error) {
      modeDescription.textContent = `No se pudieron cargar las opciones: ${error.message}`;
    }
    modeSelect.addEventListener("change", handleModeChange);
    handleModeChange(); // Aplicar estado inicial
  }

  async function loadAOIs() {
    console.log("loadAOIs: Iniciando carga de AOIs");
    try {
      const res = await fetch("/api/aois");
      console.log("loadAOIs: Response status", res.status);
      const data = await res.json();
      console.log("loadAOIs: Data recibida", data);
      state.aois = {
        list: data.aois || [],
        strategies: data.strategies || [],
      };
      console.log("loadAOIs: State actualizado", state.aois);
      hydrateAOIs();
      hydrateStrategies();
      hydrateMode4AOIs();
      hydrateMode4Strategies();
    } catch (error) {
      console.error("loadAOIs: Error", error);
      aoisList.innerHTML = `<p class="hint">Error al cargar AOIs: ${error.message}</p>`;
    }
  }

  function hydrateAOIs() {
    console.log("hydrateAOIs: Iniciando hydration, AOIs count:", state.aois.list.length);
    console.log("hydrateAOIs: aoisList element:", aoisList);
    if (!state.aois.list.length) {
      aoisList.innerHTML = '<p class="hint">No hay AOIs disponibles.</p>';
      return;
    }
    aoisList.innerHTML = "";
    state.aois.list.forEach((aoi) => {
      const div = document.createElement("div");
      div.className = "checkbox-item";
      
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = `aoi-${aoi.id}`;
      checkbox.name = "aoi";
      checkbox.value = aoi.name;
      
      const label = document.createElement("label");
      label.htmlFor = `aoi-${aoi.id}`;
      
      const title = document.createElement("div");
      title.textContent = aoi.name;
      
      const desc = document.createElement("div");
      desc.className = "aoi-description";
      desc.textContent = aoi.description;
      
      label.append(title, desc);
      div.append(checkbox, label);
      aoisList.append(div);
    });
  }

  function hydrateStrategies() {
    console.log("hydrateStrategies: Iniciando, strategies count:", state.aois.strategies.length);
    console.log("hydrateStrategies: strategySelect element:", strategySelect);
    strategySelect.innerHTML = '<option value="">Elegí una estrategia</option>';
    state.aois.strategies.forEach((strategy) => {
      const option = document.createElement("option");
      option.value = strategy.id;
      option.textContent = `${strategy.name} - ${strategy.description}`;
      strategySelect.append(option);
    });
  }

  // Modo 4: Hydrate strategies
  function hydrateMode4Strategies() {
    if (!mode4StrategySelect || !state.aois || !state.aois.strategies) return;
    mode4StrategySelect.innerHTML = '<option value="">Elegí una estrategia</option>';
    state.aois.strategies.forEach((strategy) => {
      const option = document.createElement("option");
      option.value = strategy.id;
      option.textContent = `${strategy.name} - ${strategy.description}`;
      mode4StrategySelect.append(option);
    });
  }

  // Modo 4: Hydrate AOIs
  function hydrateMode4AOIs() {
    if (!mode4AoisList || !state.aois || !state.aois.list) return;
    console.log("hydrateMode4AOIs: Iniciando, AOIs count:", state.aois.list.length);
    if (!state.aois.list.length) {
      mode4AoisList.innerHTML = '<p class="hint">No hay AOIs disponibles.</p>';
      return;
    }
    mode4AoisList.innerHTML = "";
    state.aois.list.forEach((aoi) => {
      const div = document.createElement("div");
      div.className = "checkbox-item";
      
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = `mode4-aoi-${aoi.id}`;
      checkbox.name = "mode4-aoi";
      checkbox.value = aoi.name;
      
      const label = document.createElement("label");
      label.htmlFor = `mode4-aoi-${aoi.id}`;
      
      const title = document.createElement("div");
      title.textContent = aoi.name;
      
      const desc = document.createElement("div");
      desc.className = "aoi-description";
      desc.textContent = aoi.description;
      
      label.append(title, desc);
      div.append(checkbox, label);
      mode4AoisList.append(div);
    });
  }

  function handleModeChange() {
    console.log("handleModeChange called, mode:", modeSelect.value);
    updateModeDescription();
    const modeId = modeSelect.value;
    
    // Modo 3
    if (mode3Fields) {
      if (modeId === "3") {
        mode3Fields.classList.remove("is-hidden");
        characterList.parentElement.classList.remove("is-hidden");
        if (mode4CharactersSection) mode4CharactersSection.classList.add("is-hidden");
      } else {
        mode3Fields.classList.add("is-hidden");
      }
    }
    
    // Modo 4
    if (mode4Fields) {
      if (modeId === "4") {
        mode4Fields.classList.remove("is-hidden");
        if (mode4CharactersSection) mode4CharactersSection.classList.remove("is-hidden");
        characterList.parentElement.classList.add("is-hidden");
      } else {
        mode4Fields.classList.add("is-hidden");
        if (mode4CharactersSection) mode4CharactersSection.classList.add("is-hidden");
      }
    }
    
    // Mostrar lista normal de personajes si NO es modo 4
    if (modeId !== "4") {
      characterList.parentElement.classList.remove("is-hidden");
    }
  }

  function getSelectedAOIs() {
    const checkboxes = aoisList.querySelectorAll('input[name="aoi"]:checked');
    return Array.from(checkboxes).map((cb) => cb.value);
  }

  // Modo 4: Get selected AOIs
  function getMode4SelectedAOIs() {
    const checkboxes = mode4AoisList.querySelectorAll('input[name="mode4-aoi"]:checked');
    return Array.from(checkboxes).map((cb) => cb.value);
  }

  function updatePill(text) {
    modePill.textContent = text;
  }

  function resetForm(clearStory = false) {
    form.reset();
    characterList.innerHTML = "";
    state.currentExperiment = null;
    state.experimentIndex = 0;
    experimentBanner.classList.add("is-hidden");
    nextExperimentButton.disabled = true;
    applyDefaults();
    if (clearStory) {
      storyPreview.textContent = "El cuento aparecerá aquí una vez generado.";
      storyPreview.classList.remove("error");
      if (plotSchemaPreview) {
        plotSchemaPreview.textContent = "";
      }
      if (plotSchemaPanel) {
        plotSchemaPanel.classList.add("is-hidden");
      }
    }
  }

  function enterWorkspace() {
    landingPanel.classList.remove("active");
    tabsContainer.classList.remove("is-hidden");
    setActivePanel("request-panel");
  }

  function resetFlow() {
    state.entry = null;
    updatePill("Elegí un flujo para comenzar");
    tabsContainer.classList.add("is-hidden");
    setActivePanel("landing-panel");
    tabs.forEach((tab) => tab.classList.remove("active"));
    resetForm(true);
  }

  async function ensureExperimentsLoaded() {
    if (state.experiments.length) return state.experiments;
    try {
      const res = await fetch("/api/experiments");
      const data = await res.json();
      state.experiments = data.experiments || [];
    } catch (error) {
      state.experiments = [];
      experimentTitle.textContent = `No se pudieron cargar los experimentos (${error.message}).`;
    }
    return state.experiments;
  }

  function applyExperiment(experiment) {
    if (!experiment) {
      experimentBanner.classList.remove("is-hidden");
      experimentTitle.textContent = "No hay experimentos configurados en el backend.";
      nextExperimentButton.disabled = true;
      return;
    }

    state.currentExperiment = experiment;
    form.plot.value = experiment.trama || "";
    form.genre.value = experiment.genero || "";
    form.arc.value = experiment.arco || "";
    if (aoiOptions) {
      const selected = new Set(experiment.aoi_names || []);
      const inputs = aoiOptions.querySelectorAll("input[type='checkbox']");
      inputs.forEach((input) => {
        input.checked = selected.has(input.value);
      });
    }
    if (generationMethodSelect && experiment.generation_method) {
      generationMethodSelect.value = experiment.generation_method;
    }

    characterList.innerHTML = "";
    (experiment.personajes || []).forEach((character) => addCharacterField(character));

    updateModeDescription();
    experimentBanner.classList.remove("is-hidden");
    const counter = `${state.experimentIndex + 1}/${state.experiments.length}`;
    experimentTitle.textContent = `${experiment.title || "Experimento"} · ${counter}`;
    nextExperimentButton.disabled = state.experiments.length <= 1;
  }

  function handleExperimentAdvance() {
    if (!state.experiments.length) return;
    state.experimentIndex = (state.experimentIndex + 1) % state.experiments.length;
    applyExperiment(state.experiments[state.experimentIndex]);
  }

  function enterCustomFlow() {
    state.entry = "custom";
    updatePill("Flujo: creación libre");
    enterWorkspace();
    resetForm(true);
  }

  async function enterExperimentsFlow() {
    await ensureOptions();
    state.entry = "experiments";
    updatePill("Flujo: experimentos");
    enterWorkspace();
    const experiments = await ensureExperimentsLoaded();
    if (!experiments.length) {
      experimentBanner.classList.remove("is-hidden");
      experimentTitle.textContent = "No se encontraron experimentos en el backend.";
      nextExperimentButton.disabled = true;
      return;
    }
    state.experimentIndex = 0;
    applyExperiment(experiments[0]);
  }

  startCustom.addEventListener("click", async () => {
    await ensureOptions();
    enterCustomFlow();
  });

  startExperiments.addEventListener("click", enterExperimentsFlow);
  resetFlowButton.addEventListener("click", resetFlow);
  nextExperimentButton.addEventListener("click", handleExperimentAdvance);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const trama = form.plot.value.trim();
    const genero = form.genre.value.trim();
    const arco = form.arc.value;
    const modeId = modeSelect.value || null;

    let personajes;
    if (modeId === "4") {
      // Modo 4: No usar lista normal de personajes
      personajes = [];
    } else {
      personajes = getCharacters();
    }
    const aoi_names = getSelectedAois();
    const generation_method = (generationMethodSelect && generationMethodSelect.value) || state.currentExperiment?.generation_method || null;

    const payload = {
      trama,
      genero,
      arco,
      personajes,
      aoi_names,
      strategy: state.currentExperiment?.strategy || "sequential",
      generation_method: generation_method || null,
      model: modelSelect.value || null,
      mode: modeId,
      experiment_id: state.currentExperiment?.id || null,
    };

    if (modeId === "3") {
      payload.aois = getSelectedAOIs();
      payload.interleaving_strategy = strategySelect.value || "random";
    }

    if (modeId === "4") {
      payload.aois = getMode4SelectedAOIs();
      payload.interleaving_strategy = mode4StrategySelect.value || "random";
      const charactersWithAttributes = getMode4Characters();
      if (charactersWithAttributes.length === 0) {
        storyPreview.textContent = "Error: Debes agregar al menos un personaje con sus atributos.";
        storyPreview.classList.add("error");
        return;
      }
      payload.character_attributes = charactersWithAttributes;
    }

    storyPreview.classList.remove("error");
    storyPreview.textContent = "Generando cuento...";
    if (plotSchemaPanel) {
      plotSchemaPanel.classList.add("is-hidden");
    }
    setLoading(true);

    try {
      const response = await requestStory(payload);
      const story = response?.story?.trim() || "(Respuesta vacía)";
      storyPreview.textContent = story;
      if (response?.plot_schema && plotSchemaPreview && plotSchemaPanel) {
        const schemaText = JSON.stringify(response.plot_schema, null, 2);
        plotSchemaPreview.textContent = schemaText;
        plotSchemaPanel.classList.remove("is-hidden");
      }
      setActivePanel("review-panel");
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
  resetFlow();
  ensureOptions();
  loadAOIs();
});
