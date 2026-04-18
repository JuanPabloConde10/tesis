import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

interface ChipProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  pressed?: boolean;
  hint?: ReactNode;
}

export function Chip({
  pressed = false,
  hint,
  className,
  children,
  ...props
}: ChipProps) {
  return (
    <button
      type="button"
      aria-pressed={pressed}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-[13px] transition-colors cursor-pointer",
        pressed
          ? "bg-ink border-ink text-bg"
          : "bg-surface border-line text-ink-soft hover:border-ink-mute hover:text-ink",
        className,
      )}
      {...props}
    >
      <span>{children}</span>
      {hint ? (
        <span className="font-mono text-[10px] opacity-60">{hint}</span>
      ) : null}
    </button>
  );
}
