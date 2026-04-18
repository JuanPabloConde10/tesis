import type { ReactNode } from "react";

interface Stat {
  k: string;
  v: ReactNode;
  small?: string;
}

export function SideStats({ stats }: { stats: Stat[] }) {
  return (
    <div className="mt-5 grid grid-cols-3 gap-3">
      {stats.map((s) => (
        <div
          key={s.k}
          className="rounded-md border border-line bg-surface p-4"
        >
          <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.06em] text-ink-mute">
            {s.k}
          </p>
          <p className="font-serif text-2xl font-normal leading-none tracking-tight text-ink">
            {s.v}{" "}
            {s.small ? (
              <small className="font-sans text-[13px] font-normal text-ink-mute">
                {s.small}
              </small>
            ) : null}
          </p>
        </div>
      ))}
    </div>
  );
}
