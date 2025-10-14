import { forwardRef } from "react";
import { Link } from "@tanstack/react-router";
import { tv, type VariantProps } from "tailwind-variants";

import { Button } from "@/components";
import { env } from "@/config/env";
import { useTranslation } from "@/i18n";

const helpBlockVariants = tv({
  slots: {
    root: "flex flex-col gap-2",
    header: "flex flex-col items-start gap-2 px-6 pt-6 pb-2",
    title: "text-xl font-semibold",
    container: "flex gap-3 px-6 pb-6",
    button: "mt-auto h-10 w-full text-lg font-semibold",
  },
  variants: {
    layout: {
      row: {
        container: "flex-row",
      },
      columnReverse: {
        container: "flex-col-reverse",
      },
    },
  },
  defaultVariants: {
    layout: "row",
  },
});

const { button, container, header, root, title } = helpBlockVariants();

type HelpBlockProps = {
  className?: string;
  hasCareManager?: boolean;
} & VariantProps<typeof helpBlockVariants>;

export const HelpBlock = forwardRef<HTMLDivElement, HelpBlockProps>(
  ({ className, hasCareManager = false, layout = "row", ...props }, ref) => {
    const { t } = useTranslation();

    return (
      <div className={root({ className })} data-slot="help-block" ref={ref} {...props}>
        <div className={header()}>
          <span className={title()}>{t("appointments.detail.helpSection.needHelp")}</span>
        </div>

        <div className={container({ layout })}>
          <Button className={button()} variant="outlined" asChild>
            <a href={`mailto:${env.VITE_CONTACT_SUPPORT_EMAIL}`}>{t("footer.buttons.emailUs")}</a>
          </Button>

          {hasCareManager ? (
            <Button className={button()} variant="outlined" asChild>
              <Link to="/contact-us/chat">{t("footer.buttons.messageYourCareManager")}</Link>
            </Button>
          ) : null}
        </div>
      </div>
    );
  },
);
HelpBlock.displayName = "HelpBlock";
