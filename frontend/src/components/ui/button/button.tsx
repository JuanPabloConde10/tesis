import { type ComponentProps, forwardRef } from "react";
import { Slot } from "@radix-ui/react-slot";
import { tv, type VariantProps } from "tailwind-variants";

import type { Styled } from "@/types";

const buttonVariants = tv({
  base: "inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg font-semibold whitespace-nowrap transition-all duration-300 ease-in-out focus-visible:ring-4 focus-visible:ring-background-brand-default/25 focus-visible:outline-none disabled:pointer-events-none",
  variants: {
    variant: {
      primary:
        "bg-background-brand-default text-text-default-on-neutral hover:bg-background-brand-hover active:bg-background-brand-default disabled:bg-background-disabled-default disabled:text-text-disabled-default",
      secondary:
        "bg-background-brand-secondary text-text-default-default hover:bg-background-brand-secondary-hover active:bg-background-brand-secondary disabled:bg-background-disabled-default disabled:text-text-disabled-default",
      tertiary:
        "bg-background-brand-tertiary text-text-default-default hover:bg-background-brand-tertiary-hover active:bg-background-brand-tertiary disabled:bg-background-disabled-default disabled:text-text-disabled-default",
      outlined:
        "border border-border-brand-default bg-background-default-default text-text-brand-default shadow-sm hover:bg-background-default-hover active:bg-background-default-default disabled:border-border-disabled-default disabled:text-text-disabled-default",
      elevated:
        "border border-border-brand-default bg-background-default-default text-text-brand-default shadow-md hover:bg-background-default-hover active:bg-background-default-default disabled:border-border-disabled-default disabled:text-text-disabled-default",
      plainText:
        "text-text-brand-default hover:text-text-brand-secondary active:text-text-brand-default disabled:text-text-disabled-default",
      link: "text-text-brand-default underline decoration-1 underline-offset-1 hover:text-text-brand-secondary active:text-text-brand-default disabled:text-text-disabled-default",
      dangerPrimary:
        "bg-background-danger-default text-text-default-on-neutral hover:bg-background-danger-hover focus-visible:ring-background-danger-default/25 active:bg-background-danger-default disabled:bg-background-disabled-default disabled:text-text-disabled-default",
      dangerPlainText:
        "text-text-danger-default hover:text-text-danger-secondary focus-visible:ring-background-danger-default/25 active:text-text-danger-default disabled:text-text-disabled-default",
      dangerOutlined:
        "border border-border-danger-default bg-transparent text-text-danger-default shadow-sm hover:bg-background-danger-tertiary-hover focus-visible:ring-background-danger-default/25 active:bg-transparent disabled:border-border-disabled-default disabled:text-text-disabled-default",
      iconOutlined:
        "border border-border-default-default bg-background-default-default text-icon-default-secondary hover:border-border-brand-default hover:bg-background-default-hover active:border-border-default-default active:bg-background-default-default",
      iconPlainText:
        "text-icon-default-secondary hover:text-icon-brand-default active:text-icon-brand-default disabled:text-icon-disabled-default",
    },
    size: {
      icon: "p-2",
      xl: "p-3 text-base",
      lg: "px-3 py-2 text-base",
      md: "px-2 py-1 text-base",
      sm: "px-2 py-0.5 text-base",
      xs: "px-2 py-0.5 text-sm",
      tight: "",
    },
  },
  defaultVariants: {
    variant: "primary",
    size: "xl",
  },
});

export type ButtonProps = {
  asChild?: boolean;
  isLoading?: boolean;
} & ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> &
  Styled;

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { asChild = false, children, className, disabled, isLoading = false, size, variant, ...props },
    ref,
  ) => {
    return asChild ? (
      <Slot className={buttonVariants({ variant, size, className })} ref={ref} {...props}>
        {children}
      </Slot>
    ) : (
      <button
        className={buttonVariants({ variant, size, className })}
        disabled={isLoading || disabled}
        ref={ref}
        type="button"
        {...props}
      >
        {isLoading ? <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current mr-2" /> : null}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";

export { Button, buttonVariants };
