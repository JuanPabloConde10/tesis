import type { ComponentProps } from "react";
import { Link, type LinkProps } from "@tanstack/react-router";
import { tv, type VariantProps } from "tailwind-variants";

import type { Styled } from "@/types";
import { Button } from "../button";

const cardVariants = tv({
  slots: {
    root: "flex gap-y-2 p-4 text-text-default-default",
    header:
      "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start has-[data-slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6",
    title: "truncate font-semibold whitespace-normal text-text-default-default",
    description: "truncate text-base whitespace-normal text-text-default-secondary",
    footer: "flex items-center gap-x-2",
    action: "col-start-2 row-span-2 row-start-1 self-start justify-self-end",
    content: "break-words whitespace-normal",
    iconWrapper:
      "flex size-8 shrink-0 flex-row items-center justify-center rounded-full text-icon-disabled-default",
  },
  variants: {
    variant: {
      default: {
        root: "flex-col rounded-xl bg-background-default-default",
      },
      outlined: {
        root: "flex-col rounded-xl border border-border-brand-invert bg-background-default-default",
      },
      empty: {
        root: "flex-row items-start gap-x-2 rounded-lg border border-border-neutral-default bg-background-default-secondary sm:items-center",
      },
      outlinedShadow: {
        root: "flex-col rounded-xl border border-border-brand-invert bg-background-default-default shadow-xs",
      },
    },
    withAssessments: {
      true: { root: "rounded-t-none" },
      false: { root: "" },
    },
    rounded: {
      bottom: { root: "rounded-t-none rounded-b-xl" },
      none: { root: "rounded-none" },
      all: { root: "" },
    },
    border: {
      top: { root: "border-b-0" },
      bottom: { root: "border-t-0" },
      horizontal: { root: "border-y-0" },
      all: { root: "" },
    },
  },
  defaultVariants: {
    variant: "default",
    border: "all",
    rounded: "all",
    withAssessments: false,
  },
});

const { action, content, description, footer, header, iconWrapper, root, title } = cardVariants();

type CardRootProps = ComponentProps<"div"> & VariantProps<typeof cardVariants>;

const Root = ({
  border,
  className,
  rounded,
  variant,
  withAssessments,
  ...props
}: CardRootProps) => {
  return (
    <div
      className={root({ variant, border, rounded, withAssessments, className })}
      data-slot="card"
      {...props}
    />
  );
};

type CardRootLinkProps = Styled & LinkProps & VariantProps<typeof cardVariants>;

const RootLink = ({
  border,
  className,
  rounded,
  variant,
  withAssessments,
  ...props
}: CardRootLinkProps) => {
  return (
    <Button className="items-stretch" size="tight" variant="plainText" asChild>
      <Link
        className={root({ variant, border, rounded, withAssessments, className })}
        data-slot="card"
        {...props}
      />
    </Button>
  );
};

const Header = ({ className, ...props }: ComponentProps<"div">) => {
  return <div className={header({ className })} data-slot="card-header" {...props} />;
};

const Title = ({ className, ...props }: ComponentProps<"div">) => {
  return <div className={title({ className })} data-slot="card-title" {...props} />;
};

const Description = ({ className, ...props }: ComponentProps<"p">) => {
  return <p className={description({ className })} data-slot="card-description" {...props} />;
};

const Content = ({ className, ...props }: ComponentProps<"div">) => {
  return <div className={content({ className })} data-slot="card-content" {...props} />;
};

const Footer = ({ className, ...props }: ComponentProps<"div">) => {
  return <div className={footer({ className })} data-slot="card-footer" {...props} />;
};

const Action = ({ className, ...props }: ComponentProps<"div">) => {
  return <div className={action({ className })} data-slot="card-action" {...props} />;
};

export const IconContainer = ({ className, ...props }: ComponentProps<"div">) => {
  return <div className={iconWrapper({ className })} data-slot="card-icon-wrapper" {...props} />;
};

export const Card = {
  Root,
  RootLink,
  Header,
  Title,
  Description,
  Content,
  Footer,
  Action,
  IconContainer,
};
