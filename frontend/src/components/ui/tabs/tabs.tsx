import type { ComponentProps } from "react";
import * as TabsPrimitive from "@radix-ui/react-tabs";
import { tv } from "tailwind-variants";

const tabsVariants = tv({
  slots: {
    root: "flex w-full flex-col gap-y-6",
    list: "flex w-full",
    trigger:
      "flex-1 cursor-pointer items-center justify-center gap-1.5 border-b border-border-default-default py-4 text-sm font-semibold whitespace-nowrap text-text-default-secondary transition-[color,box-shadow] hover:text-text-default-default focus-visible:ring-4 focus-visible:ring-background-brand-default/25 focus-visible:outline-none disabled:pointer-events-none data-[state=active]:border-b-4 data-[state=active]:border-border-information-secondary data-[state=active]:text-text-neutral-default",
    content: "outline-none",
  },
});

const { content, list, root, trigger } = tabsVariants();

type RootProps<T> = {
  onValueChange?: (value: T) => void;
  value?: T;
} & Omit<ComponentProps<typeof TabsPrimitive.Root>, "onValueChange" | "value">;

const Root = <T extends string>({ className, onValueChange, value, ...props }: RootProps<T>) => {
  return (
    <TabsPrimitive.Root
      className={root({ className })}
      data-slot="tabs"
      onValueChange={onValueChange as ((value: string) => void) | undefined}
      value={value}
      {...props}
    />
  );
};

const List = ({ className, ...props }: ComponentProps<typeof TabsPrimitive.List>) => {
  return <TabsPrimitive.List className={list({ className })} data-slot="tabs-list" {...props} />;
};

const Trigger = ({ className, ...props }: ComponentProps<typeof TabsPrimitive.Trigger>) => {
  return (
    <TabsPrimitive.Trigger className={trigger({ className })} data-slot="tabs-trigger" {...props} />
  );
};

const Content = ({ className, ...props }: ComponentProps<typeof TabsPrimitive.Content>) => {
  return (
    <TabsPrimitive.Content className={content({ className })} data-slot="tabs-content" {...props} />
  );
};

export const Tabs = { Root, List, Trigger, Content };
