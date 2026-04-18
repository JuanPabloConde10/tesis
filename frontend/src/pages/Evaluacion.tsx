import { useState } from "react";
import {
  AppTop,
  Button,
  DotsRating,
  PageShell,
} from "../components";

const CRITERIA = [
  { key: "coherencia", name: "Coherencia narrativa", initial: 8 },
  { key: "aois", name: "Uso de AOIs", initial: 10 },
  { key: "personajes", name: "Desarrollo de personajes", initial: 6 },
  { key: "estilo", name: "Estilo y tono", initial: 8 },
  { key: "cierre", name: "Cierre / resolución", initial: 8 },
];

const META = [
  { k: "modo", v: "3 · interleaved" },
  { k: "aois", v: "naturaleza · vínculo" },
  { k: "modelo", v: "gpt-4.1-mini" },
  { k: "tokens", v: "842" },
];

const STORY_PARAS = [
  "En una aldea pequeña rodeada de montañas, un aprendiz de botánica llamado Teo descubrió que las flores del valle reaccionaban a la música. Al principio lo tomó por casualidad: el viento movía los pétalos, las abejas dibujaban rutas que él confundía con respuestas.",
  "Pero una tarde, su hermana Aurelia tocó una melodía en el clarinete del abuelo y el valle entero se inclinó hacia ella. Las flores giraron sus corolas como quien abre una carta. Teo entendió entonces que no había casualidad: había escucha.",
  "Durante semanas, los hermanos organizaron conciertos secretos al filo del bosque. Algo antiguo despertó ahí adentro — un ser sin nombre, hecho de raíz y canto, que les pidió silencio a cambio de abundancia. La decisión era simple en apariencia: guardar el pacto, o compartir el hallazgo con el pueblo antes de que las flores se marchitaran.",
];

export default function Evaluacion() {
  const [scores, setScores] = useState<Record<string, number>>(
    Object.fromEntries(CRITERIA.map((c) => [c.key, c.initial])),
  );

  const values = CRITERIA.map((c) => scores[c.key] ?? 0);
  const avg = values.reduce((a, b) => a + b, 0) / (values.length || 1);

  return (
    <PageShell>
      <AppTop side={<span>⌘ ← cuento anterior</span>} />

      <div className="mb-8 flex items-end justify-between border-b border-line pb-5">
        <div>
          <h2 className="mb-2 max-w-[24ch] font-serif text-[32px] font-normal tracking-tight text-ink">
            El faro que <em className="italic">hablaba</em> al océano
          </h2>
          <div className="flex flex-wrap gap-4 font-mono text-[12px] text-ink-mute">
            {META.map((m) => (
              <span key={m.k}>
                <strong className="font-medium text-ink-soft">{m.k}</strong>{" "}
                {m.v}
              </span>
            ))}
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost">Regenerar</Button>
          <Button variant="ghost">Plot schema</Button>
          <Button variant="primary">Guardar evaluación</Button>
        </div>
      </div>

      <div className="grid items-start gap-10 lg:grid-cols-[1.2fr_0.8fr]">
        <article className="drop-cap font-serif text-[17px] leading-[1.7] text-ink max-w-[64ch] text-pretty">
          {STORY_PARAS.map((p, i) => (
            <p key={i} className="mb-4">
              {p}
            </p>
          ))}
          <p className="italic text-ink-mute">[…continúa — 4 párrafos más]</p>
        </article>

        <aside className="sticky top-6 border-l border-line pl-8">
          <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.1em] text-ink-mute">
            Rúbrica · 5 criterios
          </p>
          <h3 className="mb-6 text-[19px] font-semibold tracking-tight text-ink">
            Evaluá la historia
          </h3>

          <div>
            {CRITERIA.map((c) => (
              <div key={c.key} className="border-b border-line-soft py-4">
                <div className="mb-2 flex items-baseline justify-between">
                  <span className="text-[13px] font-medium text-ink">
                    {c.name}
                  </span>
                  <span className="tnum font-mono text-[14px] text-ink">
                    {scores[c.key]}
                    <span className="text-ink-mute">/10</span>
                  </span>
                </div>
                <DotsRating
                  value={scores[c.key]}
                  max={10}
                  onChange={(v) =>
                    setScores((prev) => ({ ...prev, [c.key]: v }))
                  }
                  label={c.name}
                />
              </div>
            ))}
          </div>

          <div className="mt-6 grid grid-cols-[1fr_auto] items-center gap-4 rounded-lg border border-line bg-bg-sunk p-5">
            <div>
              <p className="mb-1 font-mono text-[12px] uppercase tracking-[0.06em] text-ink-mute">
                Score final
              </p>
              <p className="m-0 text-[12px] text-ink-soft">
                Promedio simple · 5 criterios
              </p>
            </div>
            <span className="tnum font-serif text-[44px] font-normal leading-none tracking-tight text-ink">
              {avg.toFixed(1)}
              <span className="text-[19px] text-ink-mute">/10</span>
            </span>
          </div>
        </aside>
      </div>
    </PageShell>
  );
}
