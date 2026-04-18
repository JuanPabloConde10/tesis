import type { ReactNode } from "react";
import { DotsRating } from "./DotsRating";

interface Criterion {
  name: string;
  value: number;
}

interface PreviewCardProps {
  badge?: string;
  tag?: string;
  title: ReactNode;
  excerpt: string;
  criteria: Criterion[];
  max?: number;
}

export function PreviewCard({
  badge = "Ejemplo · cuento + evaluación",
  tag = "modo 3 · aoi-directo",
  title,
  excerpt,
  criteria,
  max = 10,
}: PreviewCardProps) {
  const avg =
    criteria.reduce((a, c) => a + c.value, 0) / (criteria.length || 1);

  return (
    <div className="overflow-hidden rounded-lg border border-line bg-surface">
      <div className="flex items-center justify-between border-b border-line bg-bg-sunk px-4 py-3 font-mono text-[11px] uppercase tracking-[0.06em] text-ink-mute">
        <span>
          <strong className="font-medium text-ink-soft">{badge}</strong>
        </span>
        <span>{tag}</span>
      </div>

      <div className="px-5 pt-5 pb-4">
        <h3 className="mb-3 max-w-[22ch] font-serif text-2xl font-normal leading-tight tracking-tight text-ink">
          {title}
        </h3>
        <p className="excerpt mb-4 font-serif text-[15px] leading-relaxed text-ink-soft text-pretty">
          {excerpt}
        </p>

        <div className="-mx-5 h-px bg-line-soft" />

        <div className="grid gap-2.5 py-4">
          {criteria.map((c) => (
            <div
              key={c.name}
              className="grid grid-cols-[1fr_80px_auto] items-center gap-3 text-[13px]"
            >
              <span className="text-ink">{c.name}</span>
              <DotsRating value={c.value} max={max} readOnly />
              <span className="tnum w-[30px] text-right font-mono text-[12px] text-ink-soft">
                {c.value}/{max}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-baseline justify-between border-t border-line-soft px-5 pt-3 pb-5">
        <span className="font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
          Score final · promedio
        </span>
        <span className="font-serif text-2xl font-normal tracking-tight text-ink">
          {avg.toFixed(1)}
          <span className="text-sm text-ink-mute">/{max}</span>
        </span>
      </div>
    </div>
  );
}
