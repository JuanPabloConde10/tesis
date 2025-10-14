import { type ComponentProps, type ReactNode } from "react";
import { tv, type VariantProps } from "tailwind-variants";

const iconWrapperVariants = tv({
  base: "flex items-center justify-center",
  variants: {
    size: {
      sm: "h-4 w-4",
      md: "h-5 w-5",
      lg: "h-6 w-6",
      xl: "h-8 w-8",
    },
  },
  defaultVariants: {
    size: "md",
  },
});

type IconWrapperProps = {
  children: ReactNode;
} & ComponentProps<"div"> &
  VariantProps<typeof iconWrapperVariants>;

export const IconWrapper = ({ children, className, size, ...props }: IconWrapperProps) => {
  return (
    <div className={iconWrapperVariants({ size, className })} {...props}>
      {children}
    </div>
  );
};
