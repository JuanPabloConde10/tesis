import { cn } from "../lib/cn";

interface DotsRatingProps {
  value: number;
  max?: number;
  onChange?: (v: number) => void;
  label?: string;
  readOnly?: boolean;
  size?: "sm" | "md";
}

export function DotsRating({
  value,
  max = 10,
  onChange,
  label,
  readOnly = false,
  size = "md",
}: DotsRatingProps) {
  const isInteractive = !readOnly && !!onChange;
  const height = size === "sm" ? "h-1.5" : "h-1.5";

  return (
    <div
      role={isInteractive ? "slider" : undefined}
      aria-label={label}
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
      className="flex gap-[3px]"
    >
      {Array.from({ length: max }).map((_, i) => {
        const idx = i + 1;
        const isOn = idx <= value;
        const isActive = idx === value;
        return (
          <button
            key={i}
            type="button"
            disabled={!isInteractive}
            onClick={() => onChange?.(idx)}
            aria-label={`${idx} / ${max}`}
            className={cn(
              "flex-1 min-w-[6px] rounded-[2px] border-0 p-0 transition-colors",
              height,
              isOn
                ? isActive
                  ? "bg-accent"
                  : "bg-ink"
                : "bg-line hover:bg-ink-mute",
              isInteractive ? "cursor-pointer" : "cursor-default",
            )}
          />
        );
      })}
    </div>
  );
}
