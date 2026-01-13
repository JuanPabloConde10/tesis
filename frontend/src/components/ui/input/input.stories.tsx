import type { Meta, StoryObj } from "@storybook/react-vite";

import { Icons } from "@/components";
import { SIZE } from "@/types";
import { Input } from "./input";

const meta: Meta<typeof Input> = {
  args: { placeholder: "Type your text here..." },
  argTypes: {
    disabled: { control: { type: "boolean" } },
    size: { control: { type: "select" }, options: Object.values(SIZE) },
  },
  component: Input,
  parameters: { layout: "centered" },
  tags: ["autodocs"],
  title: "Components/UI/Input",
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: (props, { updateArgs }) => {
    return (
      <Input
        {...props}
        onChange={(e) => {
          updateArgs({ value: e.target.value });
        }}
      />
    );
  },
};

export const WithIcon: Story = {
  render: (props, { updateArgs }) => {
    return (
      <Input
        {...props}
        left={<Icons.Search />}
        onChange={(e) => {
          updateArgs({ value: e.target.value });
        }}
      />
    );
  },
};
