import type { Meta, StoryObj } from "@storybook/react-vite";

import { LoadingSpinner } from "./loading-spinner";

const meta: Meta<typeof LoadingSpinner> = {
  component: LoadingSpinner,
  parameters: { layout: "centered" },
  tags: ["autodocs"],
  title: "Components/UI/LoadingSpinner",
} satisfies Meta<typeof LoadingSpinner>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: (props) => {
    return <LoadingSpinner {...props} />;
  },
};
