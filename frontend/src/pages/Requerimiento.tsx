import { useState } from "react";
import {
  AppTop,
  Button,
  CharacterBlock,
  Chip,
  Field,
  FieldGroup,
  FormAside,
  Input,
  NoteBox,
  PageShell,
  Select,
  Textarea,
  type CharacterTraits,
  type FormStep,
} from "../components";

const STEPS: FormStep[] = [
  { key: "mode", label: "Configuración del modo" },
  { key: "plot", label: "Trama & personajes" },
  { key: "arc", label: "Género & arco" },
  { key: "aois", label: "Axis of Interest" },
  { key: "review", label: "Revisar y generar" },
];

const INTERLEAVING = [
  { id: "A", label: "A · alternado" },
  { id: "B", label: "B · bloque" },
  { id: "C", label: "C · ponderado" },
  { id: "D", label: "D · greedy" },
];

const AOIS = [
  { id: "aoi-01", label: "Naturaleza" },
  { id: "aoi-04", label: "Vínculo familiar" },
  { id: "aoi-07", label: "Tensión moral" },
  { id: "aoi-02", label: "Descubrimiento" },
  { id: "aoi-05", label: "Comunidad" },
  { id: "aoi-08", label: "Pérdida" },
];

interface Character {
  id: string;
  name: string;
  traits: CharacterTraits;
}

const INITIAL_CHARS: Character[] = [
  {
    id: "1",
    name: "Aurelia, la aprendiz",
    traits: { valentia: 4, carisma: 3, bondad: 5, astucia: 4, maldad: 1 },
  },
  {
    id: "2",
    name: "Teo, su hermano menor",
    traits: { valentia: 2, carisma: 4, bondad: 4, astucia: 3, maldad: 1 },
  },
  {
    id: "3",
    name: "",
    traits: { valentia: 3, carisma: 3, bondad: 3, astucia: 3, maldad: 3 },
  },
];

export default function Requerimiento() {
  const [interleaving, setInterleaving] = useState("A");
  const [activeAois, setActiveAois] = useState(new Set(["aoi-01", "aoi-04"]));
  const [chars, setChars] = useState<Character[]>(INITIAL_CHARS);

  const toggleAoi = (id: string) => {
    setActiveAois((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const updateChar = (id: string, patch: Partial<Character>) =>
    setChars((prev) =>
      prev.map((c) => (c.id === id ? { ...c, ...patch } : c)),
    );

  const updateTrait = (id: string, trait: keyof CharacterTraits, value: number) =>
    setChars((prev) =>
      prev.map((c) =>
        c.id === id ? { ...c, traits: { ...c.traits, [trait]: value } } : c,
      ),
    );

  const removeChar = (id: string) =>
    setChars((prev) => prev.filter((c) => c.id !== id));

  const addChar = () =>
    setChars((prev) => [
      ...prev,
      {
        id: String(Date.now()),
        name: "",
        traits: { valentia: 3, carisma: 3, bondad: 3, astucia: 3, maldad: 3 },
      },
    ]);

  return (
    <PageShell narrow>
      <AppTop side={<span>⏎ para generar</span>} />

      <div className="grid items-start gap-12 lg:grid-cols-[240px_1fr]">
        <FormAside steps={STEPS} currentKey="mode" />

        <div className="min-w-0">
          <h2 className="mb-2 font-serif text-[32px] font-normal tracking-tight text-ink">
            Armá el pedido
          </h2>
          <p className="mb-10 max-w-[56ch] text-ink-soft">
            Definí los parámetros del cuento. Los campos que no completes se
            eligen por defecto desde la config del backend.
          </p>

          <NoteBox>
            <strong className="font-semibold">Ejecutando experimento</strong> —{" "}
            <em className="italic">aoi-directo / modo 3 / interleaving A</em>.
            Los campos se llenaron automáticamente.
          </NoteBox>

          {/* 01 Modo y modelo */}
          <FieldGroup legend="01 · Modo y modelo">
            <div className="mb-5 grid grid-cols-2 gap-5">
              <Field
                label="Modo de creación"
                help="desde backend"
                htmlFor="f-mode"
              >
                <Select id="f-mode" defaultValue="3">
                  <option value="1">Modo 1 · Texto libre</option>
                  <option value="2">Modo 2 · Gramática o AOI directo</option>
                  <option value="3">Modo 3 · Spans interleaved por AOI</option>
                  <option value="4">Modo 4 · Personajes con atributos</option>
                </Select>
              </Field>
              <Field label="Modelo LLM" help="opcional" htmlFor="f-model">
                <Select id="f-model" defaultValue="gpt-4.1-mini">
                  <option value="gpt-4.1-mini">gpt-4.1-mini (default)</option>
                  <option value="gpt-4.1">gpt-4.1</option>
                  <option value="claude-opus-4">claude-opus-4</option>
                </Select>
              </Field>
            </div>
            <Field label="Estrategia de interleaving">
              <div className="flex flex-wrap gap-1.5">
                {INTERLEAVING.map((i) => (
                  <Chip
                    key={i.id}
                    pressed={interleaving === i.id}
                    onClick={() => setInterleaving(i.id)}
                  >
                    {i.label}
                  </Chip>
                ))}
              </div>
            </Field>
          </FieldGroup>

          {/* 02 Trama y personajes */}
          <FieldGroup legend="02 · Trama y personajes">
            <Field
              label="Descripción de la trama"
              help="120–400 caracteres recomendado"
              htmlFor="f-plot"
            >
              <Textarea
                id="f-plot"
                rows={4}
                defaultValue="En una aldea rodeada de montañas, un aprendiz de botánica descubre que las flores del valle reaccionan a la música."
              />
            </Field>

            <Field label="Personajes" help="Atributos 1–5 · arrastrá para reordenar">
              <div>
                {chars.map((c, i) => (
                  <CharacterBlock
                    key={c.id}
                    idx={i + 1}
                    name={c.name}
                    traits={c.traits}
                    onNameChange={(name) => updateChar(c.id, { name })}
                    onTraitChange={(trait, value) =>
                      updateTrait(c.id, trait, value)
                    }
                    onRemove={() => removeChar(c.id)}
                  />
                ))}
                <button
                  type="button"
                  onClick={addChar}
                  className="border-0 bg-transparent pt-3 text-[13px] text-ink-soft hover:text-ink cursor-pointer"
                >
                  <span className="text-ink-mute">+ </span>Agregar personaje
                </button>
              </div>
            </Field>
          </FieldGroup>

          {/* 03 Género y arco */}
          <FieldGroup legend="03 · Género y arco">
            <div className="grid grid-cols-2 gap-5">
              <Field label="Género" htmlFor="f-genre">
                <Input
                  id="f-genre"
                  defaultValue="Realismo mágico"
                  placeholder="Fantasía, policial, ciencia ficción…"
                />
              </Field>
              <Field label="Arco narrativo" htmlFor="f-arc">
                <Select id="f-arc" defaultValue="viaje">
                  <option value="viaje">Viaje del héroe</option>
                  <option value="maduracion">Maduración</option>
                  <option value="busqueda">Búsqueda</option>
                  <option value="venganza">Venganza</option>
                  <option value="tragedia">Tragedia</option>
                  <option value="redencion">Redención</option>
                </Select>
              </Field>
            </div>
          </FieldGroup>

          {/* 04 AOIs */}
          <FieldGroup legend="04 · Axis of Interest">
            <Field
              label="AOIs activos"
              help="si no elegís, se seleccionan automáticamente"
            >
              <div className="flex flex-wrap gap-1.5">
                {AOIS.map((a) => (
                  <Chip
                    key={a.id}
                    pressed={activeAois.has(a.id)}
                    hint={a.id}
                    onClick={() => toggleAoi(a.id)}
                  >
                    {a.label}
                  </Chip>
                ))}
              </div>
            </Field>
          </FieldGroup>

          <div className="mt-8 flex items-center justify-between border-t border-line pt-6">
            <p className="m-0 font-mono text-[12px] text-ink-mute">
              <kbd>⌘</kbd>
              <kbd>⏎</kbd> para generar · <kbd>Esc</kbd> para volver
            </p>
            <div className="flex gap-2">
              <Button variant="ghost">Guardar borrador</Button>
              <Button variant="primary">Generar cuento</Button>
            </div>
          </div>
        </div>
      </div>
    </PageShell>
  );
}
