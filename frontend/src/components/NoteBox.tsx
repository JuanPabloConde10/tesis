import type { ReactNode } from "react";

export function NoteBox({ children }: { children: ReactNode }) {
  return (
    <div className="mb-5 rounded-r-[4px] border-l-2 border-accent bg-accent-soft px-4 py-3 text-[13px] text-ink">
      {children}
    </div>
  );
}
