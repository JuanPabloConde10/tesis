import { DotsRating } from "./DotsRating";

export interface CharacterTraits {
  valentia: number;
  carisma: number;
  bondad: number;
  astucia: number;
  maldad: number;
}

export const TRAIT_ORDER: Array<keyof CharacterTraits> = [
  "valentia",
  "carisma",
  "bondad",
  "astucia",
  "maldad",
];

const TRAIT_LABELS: Record<keyof CharacterTraits, string> = {
  valentia: "Valentía",
  carisma: "Carisma",
  bondad: "Bondad",
  astucia: "Astucia",
  maldad: "Maldad",
};

interface CharacterBlockProps {
  idx: number;
  name: string;
  placeholder?: string;
  traits: CharacterTraits;
  onNameChange?: (name: string) => void;
  onTraitChange?: (trait: keyof CharacterTraits, value: number) => void;
  onRemove?: () => void;
}

export function CharacterBlock({
  idx,
  name,
  placeholder = "Nombre del personaje…",
  traits,
  onNameChange,
  onTraitChange,
  onRemove,
}: CharacterBlockProps) {
  return (
    <div className="border-b border-line-soft first:border-t first:border-line-soft">
      <div className="grid grid-cols-[24px_1fr_auto] items-center gap-3 px-3 pt-2.5 pb-1.5">
        <span className="font-mono text-[12px] text-ink-mute">
          {String(idx).padStart(2, "0")}
        </span>
        <input
          type="text"
          value={name}
          placeholder={placeholder}
          onChange={(e) => onNameChange?.(e.target.value)}
          className="border-0 bg-transparent py-1 font-serif text-base text-ink outline-none"
        />
        <button
          type="button"
          onClick={onRemove}
          className="border-0 bg-transparent px-2 py-1 font-mono text-[12px] text-ink-mute hover:text-danger cursor-pointer"
        >
          Quitar
        </button>
      </div>
      <div
        className="grid gap-3 px-3 pb-4"
        style={{
          gridTemplateColumns: "repeat(5, minmax(0, 1fr))",
          paddingLeft: "calc(24px + 12px + 12px)",
        }}
      >
        {TRAIT_ORDER.map((t) => (
          <div key={t} className="flex flex-col gap-1">
            <div className="flex items-baseline justify-between font-mono text-[11px] uppercase tracking-[0.04em] text-ink-mute">
              <span>{TRAIT_LABELS[t]}</span>
              <span className="text-[12px] font-medium text-ink">
                {traits[t]}
                <span className="font-normal text-ink-mute">/5</span>
              </span>
            </div>
            <DotsRating
              value={traits[t]}
              max={5}
              onChange={(v) => onTraitChange?.(t, v)}
              label={`${TRAIT_LABELS[t]} ${traits[t]}/5`}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
