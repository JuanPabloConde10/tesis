import type { Meta, StoryObj } from "@storybook/react-vite";

import { Toggle } from "./toggle";

const meta: Meta<typeof Toggle> = {
  component: Toggle,
  parameters: { layout: "padded" },
  tags: ["autodocs"],
  title: "Components/UI/Toggle",
} satisfies Meta<typeof Toggle>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    return (
      <Toggle>
        <p>Toggle</p>
      </Toggle>
    );
  },
};
