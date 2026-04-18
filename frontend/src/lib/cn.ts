import { twMerge } from "tailwind-merge";

type ClassValue = string | number | false | null | undefined | ClassValue[];

export function cn(...inputs: ClassValue[]): string {
  const flatten = (arr: ClassValue[]): string[] =>
    arr.flatMap((v) => {
      if (!v && v !== 0) return [];
      if (Array.isArray(v)) return flatten(v);
      return [String(v)];
    });
  return twMerge(flatten(inputs).join(" "));
}
