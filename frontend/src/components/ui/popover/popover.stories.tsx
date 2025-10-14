import { type ComponentProps, useState } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Popover } from "./popover";

const meta = {
  component: Popover.Root,
  parameters: { layout: "centered" },
  tags: ["autodocs"],
  title: "Components/UI/Popover",
} satisfies Meta<ComponentProps<typeof Popover.Root>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [open, setOpen] = useState(false);

    return (
      <Popover.Root onOpenChange={setOpen} open={open}>
        <Popover.Trigger>Click to Open!</Popover.Trigger>

        <Popover.Content>This is visible now</Popover.Content>
      </Popover.Root>
    );
  },
};
