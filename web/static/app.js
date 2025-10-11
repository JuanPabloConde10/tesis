document.addEventListener("DOMContentLoaded", () => {
  const providerSelect = document.getElementById("provider");
  const form = document.getElementById("chat-form");
  const responseBox = document.getElementById("response");
  const submitButton = form.querySelector("button[type='submit']");

  async function loadProviders() {
    try {
      const res = await fetch("/api/providers");
      if (!res.ok) {
        throw new Error("No se pudo cargar la lista de proveedores.");
      }
      const data = await res.json();
      providerSelect.innerHTML = "";
      data.providers.forEach((provider) => {
        const option = document.createElement("option");
        option.value = provider;
        option.textContent = provider.charAt(0).toUpperCase() + provider.slice(1);
        providerSelect.append(option);
      });
      providerSelect.value = data.default;
    } catch (error) {
      providerSelect.innerHTML = "";
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "Error cargando proveedores";
      providerSelect.append(option);
      providerSelect.disabled = true;
      showError(error.message);
    }
  }

  function showError(message) {
    responseBox.classList.remove("loading");
    responseBox.textContent = message;
    responseBox.classList.add("error");
  }

  function resetResponseBox() {
    responseBox.classList.remove("error");
    responseBox.textContent = "";
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    resetResponseBox();
    responseBox.classList.add("loading");
    submitButton.disabled = true;

    const payload = {
      prompt: form.prompt.value.trim(),
      provider: providerSelect.disabled ? null : providerSelect.value || null,
      system: form.system.value.trim() || null,
      temperature: form.temperature.value ? Number(form.temperature.value) : null,
      max_tokens: form.maxTokens.value ? Number(form.maxTokens.value) : null,
    };

    if (!payload.prompt) {
      showError("El prompt no puede estar vacío.");
      submitButton.disabled = false;
      return;
    }

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) {
        const message =
          data.detail ||
          data.message ||
          "Ocurrió un error inesperado al consultar el modelo.";
        throw new Error(message);
      }

      responseBox.textContent = data.response || "(Respuesta vacía)";
    } catch (error) {
      showError(error.message);
    } finally {
      responseBox.classList.remove("loading");
      submitButton.disabled = false;
    }
  });

  loadProviders();
});
