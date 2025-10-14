import type { ComponentProps } from "react";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { tv } from "tailwind-variants";

import { Icons } from "../icons";
import { Input } from "../input";

const popoverVariants = tv({
  slots: {
    content:
      "z-50 w-72 origin-(--radix-popover-content-transform-origin) rounded-md border border-border-default-default bg-background-default-default p-4 text-text-default-default shadow-md outline-hidden data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95",
    trigger:
      "flex cursor-pointer items-center justify-between gap-2 focus-visible:ring-4 focus-visible:ring-background-brand-default/25 focus-visible:outline-none",
  },
});

const { content, trigger } = popoverVariants();

const Root = ({ ...props }: ComponentProps<typeof PopoverPrimitive.Root>) => {
  return <PopoverPrimitive.Root data-slot="popover" {...props} />;
};

const Trigger = ({
  children,
  className,
  ...props
}: ComponentProps<typeof PopoverPrimitive.Trigger>) => {
  return (
    <Input asChild>
      <PopoverPrimitive.Trigger
        className={trigger({ className })}
        data-slot="popover-trigger"
        {...props}
      >
        {children}

        <Icons.CaretDown className="size-4 opacity-50" />
      </PopoverPrimitive.Trigger>
    </Input>
  );
};

const Content = ({
  align = "center",
  className,
  sideOffset = 4,
  ...props
}: ComponentProps<typeof PopoverPrimitive.Content>) => {
  return (
    <PopoverPrimitive.Portal>
      <PopoverPrimitive.Content
        align={align}
        className={content({ className })}
        data-slot="popover-content"
        sideOffset={sideOffset}
        {...props}
      />
    </PopoverPrimitive.Portal>
  );
};

const Anchor = ({ ...props }: ComponentProps<typeof PopoverPrimitive.Anchor>) => {
  return <PopoverPrimitive.Anchor data-slot="popover-anchor" {...props} />;
};

export const Popover = { Root, Anchor, Content, Trigger };
