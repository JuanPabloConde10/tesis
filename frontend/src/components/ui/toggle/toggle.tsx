import type { ComponentProps } from "react";
import * as TogglePrimitive from "@radix-ui/react-toggle";
import { tv } from "tailwind-variants";

const toggleVariants = tv({
  slots: {
    root: "cursor-pointer rounded-sm border border-border-default-secondary px-3 py-1.5 text-sm whitespace-nowrap text-text-default-default transition-all duration-300 ease-in-out hover:bg-background-default-secondary focus-visible:ring-4 focus-visible:ring-background-brand-default/25 focus-visible:outline-none data-[state=on]:border-background-brand-default data-[state=on]:bg-background-brand-default data-[state=on]:font-semibold data-[state=on]:text-text-neutral-on-neutral",
  },
});

const { root } = toggleVariants();

export const Toggle = ({ className, ...props }: ComponentProps<typeof TogglePrimitive.Root>) => {
  return <TogglePrimitive.Root className={root({ className })} {...props} />;
};
