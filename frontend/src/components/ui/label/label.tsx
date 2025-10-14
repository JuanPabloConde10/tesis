import { type ComponentProps } from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { tv } from "tailwind-variants";

import type { Styled } from "@/types";

const labelVariants = tv({
  base: "text-sm text-text-default-default peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
});

type LabelProps = ComponentProps<typeof LabelPrimitive.Root> & Styled;

export const Label = ({ className, ...props }: LabelProps) => {
  return <LabelPrimitive.Root className={labelVariants({ className })} {...props} />;
};
