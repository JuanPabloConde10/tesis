import { useEffect, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { AppTop, PageShell } from "../components";
import { cn } from "../lib/cn";

const TOC = [
  { id: "glosario", label: "Glosario" },
  { id: "modos", label: "Modos de generación" },
  { id: "rubrica", label: "Rúbrica de evaluación" },
  { id: "aois", label: "Axis of Interest" },
  { id: "arcos", label: "Arcos narrativos" },
  { id: "experimentos", label: "Experimentos" },
];

const GLOSSARY = [
  {
    term: "Modo 1",
    strong: "Texto libre.",
    def: "Trama + personajes como prompt directo al LLM, sin schema. Máxima libertad narrativa, mínima estructura.",
  },
  {
    term: "Modo 2",
    strong: "Gramática o AOI directo.",
    def: "Schema JSON que describe AOIs y valores. Respuesta estructurada.",
  },
  {
    term: "Modo 3",
    strong: "Spans interleaved.",
    def: "Fragmentos de varios AOIs con estrategia de combinación configurable.",
  },
  {
    term: "Modo 4",
    strong: "Personajes con atributos.",
    def: "Cada personaje con rasgos numéricos 1–5 (valentía, curiosidad, etc.).",
  },
  {
    term: "AOI",
    strong: "Axis of Interest.",
    def: "Eje temático (naturaleza, vínculo, pérdida…) valor 0–1.",
  },
  {
    term: "Arco",
    strong: "Estructura narrativa.",
    def: "Plantilla: viaje del héroe, maduración, búsqueda, venganza, tragedia, redención.",
  },
  {
    term: "Rúbrica",
    strong: "5 criterios, escala 0–10.",
    def: "Coherencia, uso de AOIs, personajes, estilo, cierre. Se promedian.",
  },
  {
    term: "Experimento",
    strong: "Caso prearmado.",
    def: "Combinación trama + AOIs + arco + modo guardada en backend.",
  },
  {
    term: "Corrida",
    strong: "Una ejecución.",
    def: "Llamada al LLM + cuento resultante + evaluación. Unidad comparable.",
  },
];

const MODES = [
  {
    num: "Modo 1",
    title: "Texto libre.",
    body: [
      "Solo se envía la trama y los personajes como prompt. El LLM responde texto plano. Sirve como baseline.",
      <>
        Input: <code>plot</code>, <code>characters</code>. Output:{" "}
        <code>text/plain</code>.
      </>,
    ],
    meta: "Cuándo usarlo — Prototipado rápido, exploración de estilo, baseline.",
  },
  {
    num: "Modo 2",
    title: "Gramática o AOI directo.",
    body: [
      "Schema JSON con AOIs y valores. Respeta la distribución temática.",
      "Input: plot, aois[], arc. Output: text/plain + metadata.",
    ],
    meta: "Cuando querés controlar los ejes temáticos con precisión.",
  },
  {
    num: "Modo 3",
    title: "Spans interleaved.",
    body: [
      "Generación por fragmentos; varios spans guiados por AOIs se intercalan (secuencial, alternada, ponderada).",
      "Parámetros: strategy, span_length, weight_schema.",
    ],
    meta: "Cuentos con tensión entre múltiples ejes.",
  },
  {
    num: "Modo 4",
    title: "Personajes con atributos.",
    body: [
      "Extiende modo 2: vector 1–5 (valentía, carisma, bondad, astucia, maldad) dramatizado por el LLM en acciones y diálogo.",
      "Input adicional: characters[].traits{}.",
    ],
    meta: "Foco en personajes, consistencia interna.",
  },
];

const RUBRIC = [
  {
    num: "01",
    name: "Coherencia",
    desc: "La historia tiene causa-efecto consistente, sin saltos lógicos ni contradicciones internas.",
  },
  {
    num: "02",
    name: "Uso de AOIs",
    desc: "Los ejes temáticos declarados aparecen dramatizados en el texto, no solo mencionados.",
  },
  {
    num: "03",
    name: "Personajes",
    desc: "Los personajes actúan de forma distinguible y coherente con sus rasgos o rol declarado.",
  },
  {
    num: "04",
    name: "Estilo y tono",
    desc: "La prosa es legible, el registro sostenido, el tono adecuado al arco elegido.",
  },
  {
    num: "05",
    name: "Cierre",
    desc: "El final resuelve tensiones plantadas y no depende de recursos externos al relato.",
  },
];

const AOI_GROUPS = [
  {
    title: "Familia · vínculos",
    chips: [
      ["v01", "Amistad"],
      ["v02", "Familia"],
      ["v03", "Pareja"],
      ["v04", "Mentor–discípulo"],
      ["v05", "Rivalidad"],
    ],
  },
  {
    title: "Familia · mundo",
    chips: [
      ["m01", "Naturaleza"],
      ["m02", "Pueblo"],
      ["m03", "Ciudad"],
      ["m04", "Viaje"],
      ["m05", "Frontera"],
    ],
  },
  {
    title: "Familia · conflicto interno",
    chips: [
      ["i01", "Duelo"],
      ["i02", "Culpa"],
      ["i03", "Curiosidad"],
      ["i04", "Miedo"],
      ["i05", "Vocación"],
    ],
  },
  {
    title: "Familia · sociedad",
    chips: [
      ["s01", "Justicia"],
      ["s02", "Poder"],
      ["s03", "Tradición"],
      ["s04", "Cambio"],
      ["s05", "Trabajo"],
    ],
  },
];

const ARCS = [
  {
    term: "Viaje del héroe",
    def: "Llamado · prueba · retorno. Estructura clásica en tres actos; pico de tensión en el segundo.",
  },
  {
    term: "Maduración",
    def: "Partida de un estado ingenuo hacia uno consciente. Progresión acumulativa sin un único clímax.",
  },
  {
    term: "Búsqueda",
    def: "Objetivo concreto · obstáculos · resolución. Arco lineal con foco en el objeto deseado.",
  },
  {
    term: "Venganza",
    def: "Agravio · planificación · ejecución. Suele cerrar con ambigüedad sobre el costo.",
  },
  {
    term: "Tragedia",
    def: "Ascenso · caída. El protagonista pierde por una falla interna, no por un antagonista.",
  },
  {
    term: "Redención",
    def: "Caída · reconocimiento · reparación. Contrapeso natural de la tragedia.",
  },
];

function useActiveSection() {
  const [active, setActive] = useState<string>(TOC[0].id);
  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: "-20% 0px -70% 0px" },
    );
    TOC.forEach((t) => {
      const el = document.getElementById(t.id);
      if (el) obs.observe(el);
    });
    return () => obs.disconnect();
  }, []);
  return active;
}

function SectionHead({
  eyebrow,
  title,
  lede,
}: {
  eyebrow: string;
  title: string;
  lede: string;
}) {
  return (
    <div className="mb-8">
      <p className="mb-3 font-mono text-[12px] uppercase tracking-[0.08em] text-ink-mute">
        {eyebrow}
      </p>
      <h2 className="mb-3 font-serif text-[32px] font-normal tracking-tight text-ink">
        {title}
      </h2>
      <p className="m-0 max-w-[62ch] text-ink-soft text-pretty">{lede}</p>
    </div>
  );
}

function Callout({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="mt-6 rounded-md border border-line bg-bg-sunk p-5 text-[13px] text-ink">
      <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
        {label}
      </p>
      <p className="m-0 text-pretty">{children}</p>
    </div>
  );
}

export default function Documentacion() {
  const active = useActiveSection();

  return (
    <PageShell>
      <AppTop />

      <div className="grid items-start gap-10 lg:grid-cols-[200px_1fr]">
        <aside aria-label="Índice de contenidos" className="sticky top-6">
          <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
            En esta página
          </p>
          <ul className="m-0 list-none p-0">
            {TOC.map((t) => (
              <li key={t.id} className="border-b border-line-soft">
                <a
                  href={`#${t.id}`}
                  className={cn(
                    "block py-2.5 text-[13px] no-underline transition-colors",
                    active === t.id
                      ? "text-ink font-medium"
                      : "text-ink-soft hover:text-ink",
                  )}
                >
                  {t.label}
                </a>
              </li>
            ))}
          </ul>
        </aside>

        <main className="min-w-0">
          <nav className="mb-6 font-mono text-[12px] text-ink-mute">
            <Link to="/" className="text-ink-mute no-underline hover:text-ink">
              Taller
            </Link>
            {" / "}
            <span className="text-ink-soft">Documentación</span>
          </nav>

          <header className="mb-16">
            <p className="mb-3 font-mono text-[12px] uppercase tracking-[0.08em] text-ink-mute">
              Referencia · actualizado 04/26
            </p>
            <h1 className="mb-5 max-w-[18ch] font-serif text-[56px] font-normal leading-[1.02] tracking-tight text-ink">
              Documentación del <em className="italic text-accent">taller</em>.
            </h1>
            <p className="m-0 max-w-[62ch] text-[16px] text-ink-soft text-pretty">
              Esta página reúne los conceptos que vas a ver repetidos en la app:
              modos de generación, criterios de evaluación, axis of interest y arcos
              narrativos. Pensada para leer de corrido la primera vez y consultar
              puntualmente después.
            </p>
          </header>

          {/* Glosario */}
          <section id="glosario" className="mb-16 scroll-mt-10">
            <SectionHead
              eyebrow="01 · Conceptos"
              title="Glosario"
              lede="Vocabulario mínimo para moverse por los dos flujos. Los términos aparecen con la misma forma en los formularios, en la evaluación y en las respuestas del backend."
            />
            <dl className="m-0 grid grid-cols-1 md:grid-cols-[200px_1fr] gap-x-8 gap-y-4 border-t border-line pt-6">
              {GLOSSARY.map((g) => (
                <div key={g.term} className="contents">
                  <dt className="font-serif text-[17px] text-ink border-b border-line-soft pb-4">
                    {g.term}
                  </dt>
                  <dd className="m-0 text-[14px] text-ink-soft border-b border-line-soft pb-4 text-pretty">
                    <strong className="text-ink font-semibold">{g.strong}</strong>{" "}
                    {g.def}
                  </dd>
                </div>
              ))}
            </dl>
          </section>

          {/* Modos */}
          <section id="modos" className="mb-16 scroll-mt-10">
            <SectionHead
              eyebrow="02 · Flujos"
              title="Modos de generación"
              lede="Los cuatro modos representan niveles crecientes de estructura que le pasamos al LLM. Del texto libre al schema con atributos numéricos."
            />
            <div>
              {MODES.map((m) => (
                <div
                  key={m.num}
                  className="grid grid-cols-1 md:grid-cols-[120px_1fr_220px] gap-6 border-t border-line py-6"
                >
                  <p className="font-mono text-[12px] uppercase tracking-[0.08em] text-ink-mute">
                    {m.num}
                  </p>
                  <div>
                    <h3 className="mb-2 font-serif text-[19px] font-normal tracking-tight text-ink">
                      {m.title}
                    </h3>
                    {m.body.map((b, i) => (
                      <p
                        key={i}
                        className="mb-2 text-[14px] text-ink-soft last:mb-0"
                      >
                        {b}
                      </p>
                    ))}
                  </div>
                  <p className="m-0 text-[12px] text-ink-mute font-mono">{m.meta}</p>
                </div>
              ))}
            </div>
            <Callout label="Nota">
              Los modos no son exclusivos: un mismo experimento puede comparar la
              misma trama ejecutada en modo 1 vs modo 3 para medir el impacto de
              la estructura en los scores.
            </Callout>
          </section>

          {/* Rúbrica */}
          <section id="rubrica" className="mb-16 scroll-mt-10">
            <SectionHead
              eyebrow="03 · Evaluación"
              title="Rúbrica de criterios"
              lede="Cinco criterios, escala de 0 a 10, se promedian para el score final. La misma rúbrica se aplica a evaluación manual y automática."
            />
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {RUBRIC.map((r) => (
                <div
                  key={r.num}
                  className="rounded-md border border-line bg-surface p-4"
                >
                  <p className="mb-2 font-mono text-[11px] text-ink-mute">
                    {r.num}
                  </p>
                  <h4 className="mb-2 font-serif text-[17px] font-normal text-ink">
                    {r.name}
                  </h4>
                  <p className="m-0 text-[13px] text-ink-soft text-pretty">
                    {r.desc}
                  </p>
                </div>
              ))}
            </div>
          </section>

          {/* AOIs */}
          <section id="aois" className="mb-16 scroll-mt-10">
            <SectionHead
              eyebrow="04 · Taxonomía"
              title="Axis of Interest"
              lede="Inventario actual de AOIs agrupados por familia. Se pueden combinar libremente; cada corrida declara qué subconjunto usar."
            />
            <div className="grid gap-6 md:grid-cols-2">
              {AOI_GROUPS.map((g) => (
                <div key={g.title} className="border-t border-line pt-4">
                  <p className="mb-3 font-mono text-[12px] uppercase tracking-[0.08em] text-ink-mute">
                    {g.title}
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {g.chips.map(([code, label]) => (
                      <span
                        key={code}
                        className="inline-flex items-center gap-1.5 rounded-full border border-line bg-surface px-3 py-1.5 text-[13px] text-ink-soft"
                      >
                        {label}
                        <span className="font-mono text-[10px] text-ink-mute">
                          {code}
                        </span>
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Arcos */}
          <section id="arcos" className="mb-16 scroll-mt-10">
            <SectionHead
              eyebrow="05 · Estructura"
              title="Arcos narrativos"
              lede="Plantillas de progresión disponibles. El arco elegido condiciona la distribución de tensión a lo largo del relato."
            />
            <dl className="m-0 grid grid-cols-1 md:grid-cols-[200px_1fr] gap-x-8 gap-y-4 border-t border-line pt-6">
              {ARCS.map((a) => (
                <div key={a.term} className="contents">
                  <dt className="font-serif text-[17px] text-ink border-b border-line-soft pb-4">
                    {a.term}
                  </dt>
                  <dd className="m-0 text-[14px] text-ink-soft border-b border-line-soft pb-4 text-pretty">
                    {a.def}
                  </dd>
                </div>
              ))}
            </dl>
          </section>

          {/* Experimentos */}
          <section id="experimentos" className="mb-16 scroll-mt-10">
            <SectionHead
              eyebrow="06 · Flujo guiado"
              title="Experimentos prearmados"
              lede="Un experimento es una configuración guardada en el backend que precarga los campos del formulario. Pensados para comparar sistemáticamente una misma trama en distintos modos, o distintas distribuciones de AOIs bajo el mismo modo."
            />
            <Callout label="Tip">
              Desde la landing, el{" "}
              <strong className="font-semibold text-ink">Flujo guiado</strong>{" "}
              carga un experimento y después sigue al formulario con los campos
              ya rellenados — podés editarlos antes de ejecutar.
            </Callout>
          </section>

          <footer className="mt-16 flex flex-wrap items-center justify-between gap-4 border-t border-line pt-6 font-mono text-[12px] text-ink-mute">
            <span>
              Taller de cuentos · versión de tesis ·{" "}
              <strong className="font-medium text-ink-soft">web/</strong>
            </span>
            <Link to="/" className="text-ink-mute no-underline hover:text-ink">
              ← Volver al taller
            </Link>
          </footer>
        </main>
      </div>
    </PageShell>
  );
}
