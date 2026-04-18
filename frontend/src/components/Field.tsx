import type { InputHTMLAttributes, SelectHTMLAttributes, TextareaHTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

interface FieldProps {
  label: string;
  help?: string;
  children: ReactNode;
  htmlFor?: string;
  className?: string;
}

export function Field({ label, help, children, htmlFor, className }: FieldProps) {
  return (
    <div className={cn("mb-5 grid gap-2", className)}>
      <label
        htmlFor={htmlFor}
        className="flex items-baseline justify-between text-[13px] font-medium text-ink"
      >
        <span>{label}</span>
        {help ? (
          <span className="text-[12px] font-normal text-ink-mute">{help}</span>
        ) : null}
      </label>
      {children}
    </div>
  );
}

const inputClass =
  "w-full rounded-[6px] border border-line bg-surface px-3 py-2.5 text-[14px] text-ink transition-[border-color,box-shadow] placeholder:text-ink-mute hover:border-ink-mute focus:border-ink focus:outline-none focus:ring-[3px] focus:ring-[oklch(0.58_0.12_40_/.25)]";

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={cn(inputClass, props.className)} />;
}

export function Textarea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={cn(
        inputClass,
        "min-h-[96px] resize-y leading-[1.55] p-3",
        props.className,
      )}
    />
  );
}

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      {...props}
      className={cn(inputClass, "select-chevron pr-8", props.className)}
    />
  );
}
