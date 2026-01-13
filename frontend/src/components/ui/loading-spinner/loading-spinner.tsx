import Lottie from "lottie-react";

import loadingSpinnerAnimation from "./loading-spinner.json";

export const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center">
      <Lottie animationData={loadingSpinnerAnimation} className="size-50" />
    </div>
  );
};
