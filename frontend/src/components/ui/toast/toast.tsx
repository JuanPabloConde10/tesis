import { toast, Toaster as SonnerToaster, type ToasterProps } from "sonner";

const Toaster = (props: ToasterProps) => {
  return (
    <SonnerToaster
      icons={{
        success: null,
        info: null,
        warning: null,
        error: null,
        loading: null,
      }}
      toastOptions={{
        classNames: {
          title: "!text-text-default-on-neutral !font-semibold",
          description: "!text-text-default-on-neutral !font-normal",
          success: "!bg-background-neutral-default !text-text-default-on-neutral !p-3",
          error: "!bg-background-danger-default !text-text-default-on-neutral !p-3",
        },
      }}
      {...props}
    />
  );
};

export { toast, Toaster };
