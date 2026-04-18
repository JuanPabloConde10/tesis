import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cn } from "../lib/cn";

type Variant = "primary" | "ghost" | "accent";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const base =
  "inline-flex items-center gap-2 rounded-[6px] px-4 py-2.5 text-[13px] font-medium border transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed";

const variants: Record<Variant, string> = {
  primary:
    "bg-ink text-bg border-ink hover:bg-[oklch(0.32_0.02_75)] hover:border-[oklch(0.32_0.02_75)]",
  ghost:
    "bg-transparent text-ink-soft border-line hover:text-ink hover:border-ink-mute",
  accent: "bg-accent text-white border-accent hover:brightness-95",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(base, variants[variant], className)}
      {...props}
    />
  ),
);
Button.displayName = "Button";
