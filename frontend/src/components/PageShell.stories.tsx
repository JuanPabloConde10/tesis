import type { Meta, StoryObj } from "@storybook/react-vite";
import { PageShell } from "./PageShell";

const meta = {
  title: "Layout/PageShell",
  component: PageShell,
  parameters: { layout: "fullscreen" },
} satisfies Meta<typeof PageShell>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <p className="m-0 max-w-prose text-ink-soft">
        Story mínima para que Storybook y el docgen de Vite encuentren archivos
        <code className="font-mono text-ink">*.stories.tsx</code>.
      </p>
    ),
  },
};
