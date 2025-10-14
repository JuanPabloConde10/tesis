import type { ComponentProps } from "react";
import type { Meta, StoryObj } from "@storybook/react-vite";

import { Button } from "@/components";
import { Drawer } from "./drawer";

const meta = {
  component: Drawer.Root,
  parameters: { layout: "centered" },
  tags: ["autodocs"],
  title: "Components/UI/Drawer",
} satisfies Meta<ComponentProps<typeof Drawer.Root>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    return (
      <Drawer.Root direction="right">
        <Drawer.Trigger>Open</Drawer.Trigger>

        <Drawer.Content>
          <Drawer.Header>
            <Drawer.Title>Are you absolutely sure?</Drawer.Title>
            <Drawer.Description>This action cannot be undone.</Drawer.Description>
          </Drawer.Header>

          <Drawer.Footer>
            <Button>Submit</Button>
            <Drawer.Close>
              <Button variant="outlined">Cancel</Button>
            </Drawer.Close>
          </Drawer.Footer>
        </Drawer.Content>
      </Drawer.Root>
    );
  },
};
