import type { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "../lib/cn";

interface NavItem {
  to: string;
  label: string;
}

const DEFAULT_NAV: NavItem[] = [
  { to: "/", label: "Inicio" },
  { to: "/requerimiento", label: "Requerimiento" },
  { to: "/evaluacion", label: "Evaluación" },
  { to: "/documentacion", label: "Documentación" },
];

interface AppTopProps {
  nav?: NavItem[];
  side?: ReactNode;
}

export function AppTop({ nav = DEFAULT_NAV, side }: AppTopProps) {
  const { pathname } = useLocation();

  return (
    <header className="flex items-center justify-between border-b border-line pb-5 mb-10">
      <Link to="/" className="flex items-center gap-3 no-underline text-ink">
        <span
          aria-hidden
          className="block h-[22px] w-[22px] rounded-full"
          style={{
            background:
              "radial-gradient(circle at 35% 35%, var(--color-bg) 0 3px, transparent 3.5px), var(--color-accent)",
          }}
        />
        <span className="font-serif text-base font-medium tracking-tight">
          Taller <em className="italic font-normal text-ink-soft">de cuentos</em>
        </span>
      </Link>

      <nav aria-label="Principal" className="flex gap-1 text-[13px] text-ink-soft">
        {nav.map((item) => {
          const current = pathname === item.to;
          return (
            <Link
              key={item.to}
              to={item.to}
              aria-current={current ? "page" : undefined}
              className={cn(
                "rounded px-3 py-2 no-underline transition-colors",
                current
                  ? "text-ink bg-bg-sunk"
                  : "text-ink-soft hover:text-ink",
              )}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="flex items-center gap-4 font-mono text-[12px] text-ink-mute">
        {side ?? <span>v1.2 · rama main</span>}
        <span className="grid h-7 w-7 place-items-center rounded-full border border-line bg-bg-sunk font-sans text-[12px] font-medium text-ink-soft">
          RP
        </span>
      </div>
    </header>
  );
}
