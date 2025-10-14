import { type ComponentProps, type ElementRef, forwardRef } from "react";
import { tv } from "tailwind-variants";
import { Drawer as DrawerPrimitive } from "vaul";

const drawerVariants = tv({
  slots: {
    overlay:
      "fixed inset-0 z-50 bg-black/50 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:animate-in data-[state=open]:fade-in-0",
    header: "flex flex-col gap-0.5 md:gap-1.5 md:text-left",
    footer: "mt-auto flex flex-col gap-2",
    title: "text-xl font-semibold text-text-default-default",
    description: "text-text-default-default",
    content:
      "group/drawer-content fixed z-50 flex h-auto w-full flex-col bg-background-default-default p-4 outline-none data-[vaul-drawer-direction=bottom]:inset-x-0 data-[vaul-drawer-direction=bottom]:bottom-0 data-[vaul-drawer-direction=bottom]:mt-24 data-[vaul-drawer-direction=bottom]:max-h-[80vh] data-[vaul-drawer-direction=bottom]:rounded-t-2xl data-[vaul-drawer-direction=left]:inset-y-0 data-[vaul-drawer-direction=left]:left-0 data-[vaul-drawer-direction=right]:inset-y-0 data-[vaul-drawer-direction=right]:right-0 data-[vaul-drawer-direction=left]:sm:max-w-sm data-[vaul-drawer-direction=right]:sm:max-w-sm data-[vaul-drawer-direction=left]:md:w-1/3 data-[vaul-drawer-direction=right]:md:w-1/3",
  },
});

const { content, description, footer, header, overlay, title } = drawerVariants();

const Root = ({ ...props }: ComponentProps<typeof DrawerPrimitive.Root>) => {
  return <DrawerPrimitive.Root data-slot="drawer" {...props} />;
};

const Trigger = forwardRef<
  ElementRef<typeof DrawerPrimitive.Trigger>,
  ComponentProps<typeof DrawerPrimitive.Trigger>
>(({ ...props }, ref) => {
  return <DrawerPrimitive.Trigger data-slot="drawer-trigger" ref={ref} {...props} />;
});
Trigger.displayName = "DrawerTrigger";

const Portal = ({ ...props }: ComponentProps<typeof DrawerPrimitive.Portal>) => {
  return <DrawerPrimitive.Portal data-slot="drawer-portal" {...props} />;
};

const Close = forwardRef<
  ElementRef<typeof DrawerPrimitive.Close>,
  ComponentProps<typeof DrawerPrimitive.Close>
>(({ ...props }, ref) => {
  return <DrawerPrimitive.Close data-slot="drawer-close" ref={ref} {...props} />;
});
Close.displayName = "DrawerClose";

const Overlay = forwardRef<
  ElementRef<typeof DrawerPrimitive.Overlay>,
  ComponentProps<typeof DrawerPrimitive.Overlay>
>(({ className, ...props }, ref) => {
  return (
    <DrawerPrimitive.Overlay
      className={overlay({ className })}
      data-slot="drawer-overlay"
      ref={ref}
      {...props}
    />
  );
});
Overlay.displayName = "DrawerOverlay";

const Content = forwardRef<
  ElementRef<typeof DrawerPrimitive.Content>,
  ComponentProps<typeof DrawerPrimitive.Content>
>(({ children, className, ...props }, ref) => {
  return (
    <Portal data-slot="drawer-portal">
      <Overlay />

      <DrawerPrimitive.Content
        className={content({ className })}
        data-slot="drawer-content"
        ref={ref}
        {...props}
      >
        <div className="flex flex-1 flex-col overflow-y-auto [-webkit-overflow-scrolling:touch]">
          {children}
        </div>
      </DrawerPrimitive.Content>
    </Portal>
  );
});
Content.displayName = "DrawerContent";

const Header = forwardRef<HTMLDivElement, ComponentProps<"div">>(({ className, ...props }, ref) => {
  return <div className={header({ className })} data-slot="drawer-header" ref={ref} {...props} />;
});
Header.displayName = "DrawerHeader";

const Footer = forwardRef<HTMLDivElement, ComponentProps<"div">>(({ className, ...props }, ref) => {
  return <div className={footer({ className })} data-slot="drawer-footer" ref={ref} {...props} />;
});
Footer.displayName = "DrawerFooter";

const Title = forwardRef<
  ElementRef<typeof DrawerPrimitive.Title>,
  ComponentProps<typeof DrawerPrimitive.Title>
>(({ className, ...props }, ref) => {
  return (
    <DrawerPrimitive.Title
      className={title({ className })}
      data-slot="drawer-title"
      ref={ref}
      {...props}
    />
  );
});
Title.displayName = "DrawerTitle";

const Description = forwardRef<
  ElementRef<typeof DrawerPrimitive.Description>,
  ComponentProps<typeof DrawerPrimitive.Description>
>(({ className, ...props }, ref) => {
  return (
    <DrawerPrimitive.Description
      className={description({ className })}
      data-slot="drawer-description"
      ref={ref}
      {...props}
    />
  );
});
Description.displayName = "DrawerDescription";

export const Drawer = {
  Root,
  Close,
  Content,
  Description,
  Footer,
  Header,
  Overlay,
  Portal,
  Title,
  Trigger,
};
