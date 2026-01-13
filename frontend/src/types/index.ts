export type Styled = {
  className?: string;
};

export type ComponentVariant = {
  variant?: string;
  size?: string;
};

export type Size = "x-small" | "small" | "medium" | "large" | "x-large";

export const SIZE = {
  X_SMALL: "x-small",
  SMALL: "small", 
  MEDIUM: "medium",
  LARGE: "large",
  X_LARGE: "x-large",
} as const;

export type SvgCustomProps = {
  className?: string;
  width?: number;
  height?: number;
  fill?: string;
  stroke?: string;
};
