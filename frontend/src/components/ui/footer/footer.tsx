import type { ComponentProps, PropsWithChildren } from "react";
import { forwardRef } from "react";
import { tv } from "tailwind-variants";

import { Button, type ButtonProps } from "@/components";
import { FOOTER_ID } from "@/constants";

const footerVariants = tv({
  slots: {
    root: "mt-auto flex flex-col gap-2",
    separator: "w-full border-t border-border-neutral-default pt-6",
    actionsWrapper: "flex flex-col gap-3 px-6 pb-6",
    action: "mt-auto h-10 w-full text-lg font-semibold",
  },
});

const { action, actionsWrapper, root, separator } = footerVariants();

const Root = forwardRef<HTMLDivElement, ComponentProps<"div">>(
  ({ children, className, ...props }, ref) => {
    return (
      <div className={root({ className })} data-slot="footer" id={FOOTER_ID} ref={ref} {...props}>
        <hr className={separator()} />

        <div
          className={actionsWrapper({ className })}
          data-slot="footer-actions"
          ref={ref}
          {...props}
        >
          {children}
        </div>
      </div>
    );
  },
);
Root.displayName = "FooterRoot";

const Action = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => {
    return <Button {...props} className={action({ className })} ref={ref} variant={variant} />;
  },
);
Action.displayName = "FooterAction";

type FooterLabelProps = {
  className?: string;
};

const Label = forwardRef<HTMLDivElement, PropsWithChildren<FooterLabelProps>>(
  ({ className, ...props }, ref) => {
    return <div className={className} data-slot="footer-label" ref={ref} {...props} />;
  },
);
Label.displayName = "FooterLabel";

export const Footer = { Root, Action, Label };
