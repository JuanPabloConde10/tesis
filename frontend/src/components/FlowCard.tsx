import { cn } from "../lib/cn";

interface FlowCardProps {
  idx: string;
  title: string;
  description: string;
  selected?: boolean;
  onSelect?: () => void;
}

export function FlowCard({
  idx,
  title,
  description,
  selected = false,
  onSelect,
}: FlowCardProps) {
  return (
    <button
      type="button"
      role="radio"
      aria-checked={selected}
      onClick={onSelect}
      className={cn(
        "grid w-full grid-cols-[1fr_auto] items-center gap-5 rounded-lg border bg-surface px-6 py-5 text-left transition-[border-color,background,box-shadow] cursor-pointer",
        selected
          ? "border-ink shadow-[inset_3px_0_0_var(--color-accent)]"
          : "border-line hover:border-ink",
      )}
    >
      <div>
        <p className="mb-1 font-mono text-[11px] tracking-[0.08em] text-ink-mute">
          {idx}
        </p>
        <p className="mb-1 text-base font-semibold tracking-tight text-ink">
          {title}
        </p>
        <p className="m-0 text-[13px] text-ink-soft">{description}</p>
      </div>
      <span className="font-mono text-base text-ink-mute">⟶</span>
    </button>
  );
}
