import { type ComponentProps, forwardRef, type ReactNode } from "react";
import { Slot } from "@radix-ui/react-slot";
import { tv } from "tailwind-variants";

import { IconWrapper } from "@/components/ui/icon-wrapper";
import { type Styled } from "@/types";

const inputVariants = tv({
  slots: {
    container: "relative flex w-full flex-col gap-1.5",
    input:
      "flex w-full rounded-md border border-border-default-default px-3 py-2 text-sm font-normal text-text-default-default transition-colors placeholder:text-text-default-tertiary focus-visible:outline-border-brand-default disabled:cursor-not-allowed disabled:bg-background-disabled-default disabled:text-text-disabled-default",
    wrapper: "relative flex flex-row items-center rounded-md",
    leftIcon:
      "pointer-events-none absolute top-1/2 left-2 flex -translate-y-1/2 items-center text-text-default-default",
    rightIcon:
      "absolute top-1/2 right-2 flex -translate-y-1/2 items-center text-text-default-default",
  },
  variants: {
    left: {
      true: { input: "pl-10" },
    },
    right: {
      true: { input: "pr-10" },
    },
    error: {
      true: { input: "border-border-danger-default" },
    },
  },
});

const { container, input, leftIcon, rightIcon, wrapper } = inputVariants();

type InputProps = {
  asChild?: boolean;
  containerClassName?: string;
  left?: ReactNode;
  right?: ReactNode;
  hasError?: boolean;
} & ComponentProps<"input"> &
  Styled;

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ asChild, className, containerClassName, hasError, left, right, ...props }, ref) => {
    if (asChild) {
      return <Slot className={input({ className, error: !!hasError })} ref={ref} {...props} />;
    }

    return (
      <div className={container({ className: containerClassName })}>
        <div className={wrapper()}>
          {left ? (
            <IconWrapper className={leftIcon()} size="md">
              {left}
            </IconWrapper>
          ) : null}

          <input
            className={input({ className, left: !!left, right: !!right, error: !!hasError })}
            ref={ref}
            {...props}
          />

          {right ? (
            <IconWrapper className={rightIcon()} size="md">
              {right}
            </IconWrapper>
          ) : null}
        </div>
      </div>
    );
  },
);

Input.displayName = "Input";

export { Input };
