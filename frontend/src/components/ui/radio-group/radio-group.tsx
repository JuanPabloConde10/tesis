import type { ComponentProps, ElementRef } from "react";
import { forwardRef } from "react";
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group";
import { tv } from "tailwind-variants";

import { Icons } from "@/components";

const radioGroupVariants = tv({
  slots: {
    root: "grid gap-4",
    item: "peer aspect-square size-4 shrink-0 cursor-pointer rounded-full border border-border-default-tertiary shadow-xs transition-[box-shadow] outline-none focus-visible:ring-4 focus-visible:ring-background-brand-default/25 disabled:cursor-not-allowed disabled:border-border-disabled-default disabled:bg-background-disabled-default data-[state=checked]:border-background-brand-default data-[state=checked]:bg-background-brand-default data-[state=checked]:text-icon-default-on-neutral data-[state=checked]:disabled:border-border-disabled-default data-[state=checked]:disabled:bg-background-disabled-default",
    indicatorWrapper:
      "relative flex items-center justify-center data-[disabled]:[&_svg]:bg-icon-disabled-on-disabled data-[disabled]:[&_svg]:text-icon-disabled-on-disabled",
    indicator:
      "absolute top-1/2 left-1/2 size-2 -translate-x-1/2 -translate-y-1/2 rounded-full bg-icon-default-on-neutral",
  },
});

const { indicator, indicatorWrapper, item, root } = radioGroupVariants();

const Root = forwardRef<
  ElementRef<typeof RadioGroupPrimitive.Root>,
  ComponentProps<typeof RadioGroupPrimitive.Root>
>(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Root
      className={root({ className })}
      data-slot="radio-group"
      ref={ref}
      {...props}
    />
  );
});

Root.displayName = "RadioGroupRoot";

const Indicator = forwardRef<
  ElementRef<typeof RadioGroupPrimitive.Indicator>,
  ComponentProps<typeof RadioGroupPrimitive.Indicator>
>(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Indicator
      className={indicatorWrapper({ className })}
      data-slot="radio-group-indicator"
      ref={ref}
      {...props}
    >
      <Icons.Circle className={indicator()} />
    </RadioGroupPrimitive.Indicator>
  );
});

Indicator.displayName = "RadioGroupIndicator";

const Item = forwardRef<
  ElementRef<typeof RadioGroupPrimitive.Item>,
  ComponentProps<typeof RadioGroupPrimitive.Item>
>(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Item
      className={item({ className })}
      data-slot="radio-group-item"
      ref={ref}
      {...props}
    />
  );
});

Item.displayName = "RadioGroupItem";

export const RadioGroup = { Root, Item, Indicator };
