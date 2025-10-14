import type { Meta, StoryObj } from "@storybook/react-vite";

import { TextArea } from "./text-area";

const meta: Meta<typeof TextArea> = {
  args: { placeholder: "Type your text here..." },
  argTypes: {
    disabled: { control: { type: "boolean" } },
  },
  component: TextArea,
  parameters: { layout: "centered" },
  tags: ["autodocs"],
  title: "Components/UI/TextArea",
} satisfies Meta<typeof TextArea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: (props, { updateArgs }) => {
    return (
      <TextArea
        {...props}
        onChange={(e) => {
          updateArgs({ value: e.target.value });
        }}
      />
    );
  },
};
