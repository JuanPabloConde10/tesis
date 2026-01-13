import type { ComponentProps, ElementType, JSX, PropsWithChildren } from "react";
import type { IconProps } from "@iconify/react";
import { Icon, loadIcons } from "@iconify/react";
import { tv, type VariantProps } from "tailwind-variants";

import { SIZE, type Size, type Styled, type SvgCustomProps } from "@/types";

const PHOSPHOR_ICON_PREFIX = "ph:";

const AVAILABLE_ICONIFY_ICONS = {
  Check: "check",
  CaretDown: "caret-down",
  CaretRight: "caret-right",
  CaretUp: "caret-up",
  CaretLeft: "caret-left",
  Circle: "circle",
  ChatCircleDots: "chat-circle-dots",
  LoaderCircle: "loader-circle",
  LogOut: "log-out",
  MoreHorizontal: "more-horizontal",
  Search: "search",
  Slash: "slash",
  X: "x",
  Plus: "plus",
  Eye: "eye",
  EyeSlash: "eye-slash",
  Lock: "lock",
  CalendarDotsFill: "calendar-dots-fill",
  CalendarDots: "calendar-dots",
  CalendarBlank: "calendar-blank",
  Clock: "clock",
  User: "user",
  House: "house",
  SignOut: "sign-out",
  List: "list",
  BookBookmark: "book-bookmark",
  BookBookmarkFill: "book-bookmark-fill",
  WarningCircle: "warning-circle",
  CheckCircle: "check-circle",
  XCircle: "x-circle",
  FirstAid: "first-aid",
  SparkleFill: "sparkle-fill",
  Info: "info",
  LightningFill: "lightning-fill",
  MagnifyingGlass: "magnifying-glass",
  MagnifyingGlassMinus: "magnifying-glass-minus",
  MagnifyingGlassPlus: "magnifying-glass-plus",
  Phone: "phone",
  Gavel: "gavel",
};

export const initializeIcons = () => {
  return loadIcons(
    Object.values(AVAILABLE_ICONIFY_ICONS).map((icon) => {
      return `${PHOSPHOR_ICON_PREFIX}${icon}`;
    }),
  );
};

const iconsVariants = tv({
  slots: {
    icon: "size-4 shrink-0",
    wrapper: "flex shrink-0 flex-row items-center justify-center",
  },
  variants: {
    size: {
      [SIZE.X_SMALL]: { wrapper: "size-4" },
      [SIZE.SMALL]: { wrapper: "size-5" },
      [SIZE.MEDIUM]: { wrapper: "size-6" },
      [SIZE.LARGE]: { wrapper: "size-9" },
      [SIZE.X_LARGE]: { wrapper: "size-10" },
    },
    variant: {
      none: { wrapper: "" },
      primary: { wrapper: "size-8 rounded-full bg-background-default-default" },
      secondary: { wrapper: "size-8 rounded-full bg-background-default-secondary" },
    },
  },
  defaultVariants: {
    size: SIZE.MEDIUM,
    variant: "none",
  },
});

const { icon, wrapper } = iconsVariants();

export type IconifyIconProps = Omit<IconProps, "icon">;

const iconifyIcons = Object.fromEntries(
  Object.entries(AVAILABLE_ICONIFY_ICONS).map(([key, value]) => {
    return [
      key,
      ({ className, ...rest }: IconifyIconProps) => {
        return (
          <Icon
            className={icon({ className })}
            icon={`${PHOSPHOR_ICON_PREFIX}${value}`}
            {...rest}
          />
        );
      },
    ];
  }),
) as Record<keyof typeof AVAILABLE_ICONIFY_ICONS, (props: IconifyIconProps) => JSX.Element>;

export const Icons = {
  ...iconifyIcons,

  TesisLogoAndName: (props: SvgCustomProps) => {
    return (
      <svg
        fill="none"
        height={32}
        viewBox="24.96 26.53 294.5 45.13"
        width={200}
        xmlns="http://www.w3.org/2000/svg"
        {...props}
      >
        <path
          d="M113.71 56.463C110.943 67.0642 97.5151 70.255 89.3048 63.4162C82.3146 57.5966 81.5022 46.421 87.297 39.4709C95.0193 30.2041 110.606 32.3386 113.71 44.4162L109.692 44.268C104.274 33.0707 88.6654 36.6445 87.4916 48.9353C86.4939 59.3851 96.8664 67.3329 106.028 60.9852C107.443 60.0029 109.185 58.2391 109.386 56.4661H113.71V56.463Z"
          fill="currentColor"
        />
        <path
          d="M254.255 56.463C251.528 66.9375 238.23 70.2179 230.014 63.5613C222.816 57.7294 221.998 46.5599 227.842 39.4708C235.493 30.1886 251.167 32.3879 254.255 44.4162L250.237 44.2679C246.07 34.7695 232.126 35.6035 228.84 45.4139C226.854 51.3415 228.367 58.1557 233.893 61.538C239.5 64.9667 247.747 62.7891 249.931 56.466H254.255V56.463Z"
          fill="currentColor"
        />
        <path
          d="M319.432 55.5364H299.663C299.493 63.5984 311.249 66.8634 314.49 59.2431H319.123C315.345 70.6659 297.328 68.9855 295.728 57.155C293.142 38.0593 320.272 37.1017 319.432 55.5364ZM315.107 52.1386C313.807 43.9035 301.294 43.7583 299.972 52.1386H315.107Z"
          fill="currentColor"
        />
        <path
          d="M140.275 55.5363H120.506C120.299 63.5397 132.037 66.8974 135.333 59.243H139.657C137.773 65.6216 130.826 68.3615 124.589 66.434C120.904 65.2942 117.13 61.3373 116.571 57.4638C113.778 38.1457 140.89 36.904 140.275 55.5363ZM135.95 52.1385C134.18 43.7089 122.606 43.8849 120.506 52.1385H135.95Z"
          fill="currentColor"
        />
        <path
          d="M215.335 66.3444L211.354 66.3135L211.008 63.8764C206.161 68.6395 193.697 68.3553 193.697 59.7064C193.697 55.9873 196.005 53.6088 199.508 52.8335C202.09 52.2621 210.767 52.608 211.004 49.1855C211.341 44.3174 198.97 44.5367 198.933 49.9392L194.951 49.9732C195.671 43.332 201.262 41.7289 207.162 42.2416C210.526 42.5351 214.325 44.6417 214.72 48.2743C215.347 54.0629 213.837 60.5867 215.335 66.3444ZM211.008 53.9919C207.965 55.6382 204.512 55.2089 201.358 55.9224C195.702 57.2012 196.53 62.7057 201.586 63.2586C208.079 63.966 211.95 60.6701 211.008 53.9919Z"
          fill="currentColor"
        />
        <path
          d="M277.419 66.3445L273.697 66.2086L272.943 63.8764C267.689 69.8349 252.798 66.9993 256.353 57.1704C258.877 50.1894 270.417 53.6428 272.625 50.5848C272.863 50.2543 273.036 49.8929 273.089 49.4821C273.685 44.8085 264.189 44.7684 262.018 47.6998C261.582 48.2898 261.425 49.7354 260.853 49.9331L257.341 49.9763C257.036 47.6689 258.923 44.9105 260.761 43.6626C264.928 40.83 276.103 41.7011 276.805 47.9654C277.459 53.8189 275.971 60.4508 277.419 66.3445ZM273.098 53.9919C272.004 54.31 271.18 54.8074 270.021 55.0854C267.047 55.7958 259.924 55.0854 259.791 59.3944C259.633 64.4911 268.295 64.0278 271.223 61.535C271.763 61.0748 273.101 59.3944 273.101 58.7797V53.9919H273.098Z"
          fill="currentColor"
        />
        <path
          d="M163.442 42.8718V59.3975C163.466 59.9504 164.072 60.8555 164.229 61.081C166.188 63.9567 171.55 63.9876 173.802 61.4146C174.417 60.7103 175.492 58.3998 175.492 57.5442V42.8718H179.198V66.3476H175.488V63.8764C171.102 68.9886 162.379 67.7036 160.115 61.1829C159.948 60.7041 159.429 59.589 159.429 58.4708V42.8718H163.445H163.442Z"
          fill="currentColor"
        />
        <path d="M189.079 32.3695H185.063V66.3475H189.079V32.3695Z" fill="currentColor" />
        <path
          d="M144.599 42.8717H148.309L148.46 45.034C150.295 42.5845 153.097 42.0717 156.031 42.254L156.013 45.9483C153.375 46.2294 151.101 46.5228 149.415 48.7685C149.158 49.1083 148.309 50.4705 148.309 50.7516V66.3506H144.602V42.8748L144.599 42.8717Z"
          fill="currentColor"
        />
        <path
          d="M282.982 42.8717H286.692L286.844 45.034C288.715 42.742 291.523 42.0037 294.415 42.2539L294.396 45.9483C291.9 46.2139 289.333 46.5475 287.792 48.7623C287.573 49.0804 286.689 50.8535 286.689 51.0573V66.3475H282.982V42.8717Z"
          fill="currentColor"
        />
        <path
          d="M53.0492 26.5345H41.7561C41.0737 26.5345 40.5205 27.0877 40.5205 27.77V39.0631C40.5205 39.7455 41.0737 40.2987 41.7561 40.2987H53.0492C53.7315 40.2987 54.2847 39.7455 54.2847 39.0631V27.77C54.2847 27.0877 53.7315 26.5345 53.0492 26.5345Z"
          fill="#3388D6"
        />
        <path
          d="M53.0492 57.8963H41.7561C41.0737 57.8963 40.5205 58.4494 40.5205 59.1318V70.4249C40.5205 71.1073 41.0737 71.6605 41.7561 71.6605H53.0492C53.7315 71.6605 54.2847 71.1073 54.2847 70.4249V59.1318C54.2847 58.4494 53.7315 57.8963 53.0492 57.8963Z"
          fill="#3388D6"
        />
        <path
          d="M56.5396 47.5175C56.5396 44.5274 58.9644 42.1026 61.9544 42.1026H69.3987C69.896 42.1026 70.3007 42.5072 70.3007 43.0046V54.9618C70.3007 55.4591 69.896 55.8637 69.3987 55.8637H57.4415C56.9442 55.8637 56.5396 55.4591 56.5396 54.9618V47.5175Z"
          fill="#3388D6"
        />
        <path
          d="M38.7172 50.452C38.7172 53.442 36.2924 55.8668 33.3023 55.8668H25.858C25.3607 55.8668 24.9561 55.4622 24.9561 54.9649V43.0077C24.9561 42.5104 25.3607 42.1057 25.858 42.1057H37.8152C38.3125 42.1057 38.7172 42.5104 38.7172 43.0077V50.452Z"
          fill="#3388D6"
        />
        <path
          d="M41.4225 40.2986H53.3797C53.877 40.2986 54.2816 39.894 54.2816 39.3967V35.3286C52.2399 34.3216 49.9417 33.7563 47.5138 33.7563C45.0859 33.7563 42.6179 34.3679 40.5205 35.4459V39.3967C40.5205 39.894 40.9252 40.2986 41.4225 40.2986Z"
          fill="#30E874"
        />
        <path
          d="M53.3797 57.8963H41.4225C40.9252 57.8963 40.5205 58.3009 40.5205 58.7982V62.7489C42.6179 63.827 44.9933 64.4386 47.5138 64.4386C50.0344 64.4386 52.2399 63.8702 54.2816 62.8663V58.7982C54.2816 58.3009 53.877 57.8963 53.3797 57.8963Z"
          fill="#30E874"
        />
        <path
          d="M61.1952 42.1582C58.5634 42.5258 56.5371 44.7869 56.5371 47.5206V54.9649C56.5371 55.4622 56.9418 55.8668 57.4391 55.8668H61.2817C62.2887 53.8251 62.8539 51.5269 62.8539 49.099C62.8539 46.6711 62.2516 44.2433 61.1921 42.1582H61.1952Z"
          fill="#30E874"
        />
        <path
          d="M38.7166 50.452V43.0077C38.7166 42.5104 38.312 42.1057 37.8147 42.1057H33.864C32.7859 44.2031 32.1743 46.5785 32.1743 49.099C32.1743 51.6196 32.7365 53.8127 33.7373 55.8483C36.5235 55.6259 38.7166 53.2969 38.7166 50.452Z"
          fill="#30E874"
        />
        <path
          d="M47.5138 56.0892C51.3761 56.0892 54.5071 52.9582 54.5071 49.0959C54.5071 45.2336 51.3761 42.1026 47.5138 42.1026C43.6515 42.1026 40.5205 45.2336 40.5205 49.0959C40.5205 52.9582 43.6515 56.0892 47.5138 56.0892Z"
          fill="#30E874"
        />
      </svg>
    );
  },
} as const;

type IconWrapperProps<TElement extends ElementType> = {
  size?: Size;
  as?: TElement;
} & VariantProps<typeof iconsVariants> &
  Styled &
  PropsWithChildren;

export const IconWrapper = <TElement extends ElementType = "div">({
  as,
  children,
  className,
  size,
  variant,
  ...rest
}: Omit<ComponentProps<TElement>, keyof IconWrapperProps<TElement>> &
  IconWrapperProps<TElement>) => {
  const Component = as ?? "div";

  return (
    <Component className={wrapper({ size, variant, className })} {...rest}>
      {children}
    </Component>
  );
};
