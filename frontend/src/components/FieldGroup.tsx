import type { ReactNode } from "react";

interface FieldGroupProps {
  legend: string;
  children: ReactNode;
}

export function FieldGroup({ legend, children }: FieldGroupProps) {
  return (
    <fieldset className="m-0 mb-10 border-0 p-0">
      <legend className="mb-5 block w-full border-b border-line pb-3 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-mute">
        {legend}
      </legend>
      {children}
    </fieldset>
  );
}
