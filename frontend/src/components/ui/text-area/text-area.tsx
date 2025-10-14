import { type ComponentProps, forwardRef } from "react";

import { Input } from "@/components/ui/input";

type TextAreaProps = { hasError?: boolean } & ComponentProps<"textarea">;

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  ({ className, hasError, ...props }, ref) => {
    return (
      <Input className={className} hasError={hasError} asChild>
        <textarea ref={ref} {...props} />
      </Input>
    );
  },
);

TextArea.displayName = "TextArea";
