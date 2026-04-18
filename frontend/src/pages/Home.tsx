import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  AppTop,
  FlowCard,
  PageShell,
  PreviewCard,
  SideStats,
} from "../components";

type Flow = "manual" | "guided";

const FLOWS: Array<{ id: Flow; idx: string; title: string; description: string }> = [
  {
    id: "manual",
    idx: "Flujo manual · 00",
    title: "Crear tu propia historia",
    description:
      "Trama libre, personajes, arco y AOIs definidos por vos. Ideal para redactar rápido.",
  },
  {
    id: "guided",
    idx: "Flujo guiado · 01",
    title: "Correr experimentos del backend",
    description:
      "Reproducí casos prearmados para comparar modos, estrategias y modelos.",
  },
];

const HOWTO = [
  {
    num: "01 — Configurar",
    title: "Elegís modo, modelo y parámetros",
    desc:
      "Modo de creación, modelo LLM, estrategia de interleaving y qué AOIs querés activos.",
  },
  {
    num: "02 — Generar",
    title: "El backend arma el cuento",
    desc:
      "Se construye la trama, se personajes, género y arco, y se envía al LLM con el schema definido.",
  },
  {
    num: "03 — Evaluar",
    title: "Puntuás contra la rúbrica",
    desc:
      "Asignás 0 a 10 a cada criterio. El score final es el promedio simple y queda en la evaluación.",
  },
];

export default function Home() {
  const [selected, setSelected] = useState<Flow>("manual");
  const navigate = useNavigate();

  return (
    <PageShell>
      <AppTop side={<span>v1.2 · rama main</span>} />

      <div className="grid items-start gap-12 pt-10 pb-8 lg:grid-cols-[minmax(0,620px)_minmax(320px,1fr)]">
        {/* LEAD */}
        <div className="min-w-0">
          <p className="mb-4 inline-flex items-center gap-2 font-mono text-[12px] uppercase tracking-[0.1em] text-ink-mute">
            <span className="block h-1.5 w-1.5 rounded-full bg-accent" />
            Taller narrativo · sesión nueva
          </p>
          <h1 className="mb-5 max-w-[14ch] font-serif text-[44px] font-normal leading-[1.05] tracking-tight text-ink">
            Generá, leé y <em className="italic text-accent">evaluá</em> cuentos en un solo lugar.
          </h1>
          <p className="mb-8 max-w-[40ch] text-base text-ink-soft">
            Armá una historia desde cero o cargá un experimento prearmado del backend.
            Después, puntuá cada cuento contra los criterios y comparálos entre sí.
          </p>

          <div
            role="radiogroup"
            aria-label="Elegí un flujo"
            className="grid gap-3"
          >
            {FLOWS.map((f) => (
              <FlowCard
                key={f.id}
                idx={f.idx}
                title={f.title}
                description={f.description}
                selected={selected === f.id}
                onSelect={() => {
                  setSelected(f.id);
                  navigate("/requerimiento", { state: { flow: f.id } });
                }}
              />
            ))}
          </div>

          {/* How it works */}
          <section aria-label="Cómo funciona" className="mt-12 border-t border-line pt-8">
            <p className="mb-5 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
              Cómo funciona
            </p>
            <div className="grid gap-8 md:grid-cols-3">
              {HOWTO.map((s) => (
                <div key={s.num}>
                  <p className="border-b border-line pb-2 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
                    {s.num}
                  </p>
                  <h4 className="mt-3 mb-2 font-serif text-[19px] font-normal tracking-tight text-ink">
                    {s.title}
                  </h4>
                  <p className="m-0 max-w-[34ch] text-[13px] text-ink-soft">
                    {s.desc}
                  </p>
                </div>
              ))}
            </div>
          </section>

          {/* Docs CTA */}
          <Link
            to="/documentacion"
            className="mt-12 grid grid-cols-[1fr_auto] items-center gap-6 border-y border-line px-6 py-6 text-ink no-underline transition-colors hover:bg-bg-sunk focus-visible:outline-2 focus-visible:outline-accent focus-visible:outline-offset-4 group"
          >
            <div>
              <p className="mb-2 font-mono text-[12px] uppercase tracking-[0.08em] text-ink-soft">
                <span className="mr-2 inline-block h-1.5 w-1.5 translate-y-0.5 rounded-full bg-accent" />
                Documentación
              </p>
              <h3 className="mb-2 font-serif text-[19px] font-normal leading-snug tracking-tight">
                ¿Primera vez? Leé el <em className="italic text-accent">glosario</em> y la guía de modos.
              </h3>
              <p className="m-0 max-w-[62ch] text-[13px] text-ink-soft text-pretty">
                Conceptos, modos de generación, criterios de evaluación y referencia de AOIs — todo en una página aparte.
              </p>
            </div>
            <span className="font-mono text-[19px] text-ink-soft transition-[transform,color] group-hover:translate-x-1 group-hover:text-accent">
              ⟶
            </span>
          </Link>

          {/* Foot */}
          <div className="mt-12 flex flex-wrap items-center justify-between gap-6 border-t border-line pt-6 font-mono text-[12px] text-ink-mute">
            <span>
              <strong className="font-medium text-ink-soft">Atajos</strong> ·{" "}
              <kbd>⌘</kbd>
              <kbd>K</kbd> buscar · <kbd>⌘</kbd>
              <kbd>⏎</kbd> generar · <kbd>Tab</kbd> avanzar
            </span>
            <span>
              Taller de cuentos · versión de tesis ·{" "}
              <strong className="font-medium text-ink-soft">web/</strong>
            </span>
          </div>
        </div>

        {/* SIDE */}
        <aside aria-label="Ejemplo de salida" className="sticky top-6 min-w-0">
          <PreviewCard
            title={
              <>
                El faro que <em className="italic">hablaba</em> al océano
              </>
            }
            excerpt="En una aldea pequeña rodeada de montañas, un aprendiz de botánica llamado Teo descubrió que las flores del valle reaccionaban a la música. Al principio lo tomó por casualidad: el viento movía los pétalos, las abejas dibujaban rutas que él confundía con respuestas."
            criteria={[
              { name: "Coherencia narrativa", value: 8 },
              { name: "Uso de AOIs", value: 10 },
              { name: "Personajes", value: 6 },
              { name: "Estilo y tono", value: 8 },
              { name: "Cierre", value: 8 },
            ]}
          />
          <SideStats
            stats={[
              { k: "Modos", v: "4" },
              { k: "AOIs", v: "12", small: "activos" },
              { k: "Arcos", v: "6" },
            ]}
          />
        </aside>
      </div>
    </PageShell>
  );
}
