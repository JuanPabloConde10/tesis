import type { ReactNode } from "react";
import { cn } from "../lib/cn";

interface PageShellProps {
  children: ReactNode;
  narrow?: boolean;
}

export function PageShell({ children, narrow = false }: PageShellProps) {
  return (
    <div
      className={cn(
        "min-h-screen bg-bg",
        narrow ? "px-20 py-10" : "px-12 py-10",
        "max-w-[1440px] mx-auto",
      )}
    >
      {children}
    </div>
  );
}
