import { cn } from "../lib/cn";

export interface FormStep {
  label: string;
  key: string;
}

interface FormAsideProps {
  steps: FormStep[];
  currentKey: string;
}

export function FormAside({ steps, currentKey }: FormAsideProps) {
  return (
    <aside className="sticky top-6 text-[13px]">
      <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
        Secciones
      </p>
      <ol className="m-0 list-none p-0">
        {steps.map((s, i) => {
          const current = s.key === currentKey;
          const num = String(i + 1).padStart(2, "0");
          return (
            <li
              key={s.key}
              aria-current={current ? "step" : undefined}
              className={cn(
                "grid grid-cols-[24px_1fr] items-baseline gap-3 py-2",
                current ? "text-ink font-medium" : "text-ink-soft",
              )}
            >
              <span
                className={cn(
                  "pt-0.5 font-mono text-[11px]",
                  current ? "text-accent" : "text-ink-mute",
                )}
              >
                {num}
              </span>
              <span>{s.label}</span>
            </li>
          );
        })}
      </ol>

      <p className="mt-8 mb-3 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
        Atajos
      </p>
      <p className="m-0 font-mono text-[12px] leading-relaxed text-ink-soft">
        <kbd>⌘</kbd>
        <kbd>⏎</kbd> generar · <kbd>⌘</kbd>
        <kbd>K</kbd> buscar · <kbd>Tab</kbd> avanzar
      </p>
    </aside>
  );
}
