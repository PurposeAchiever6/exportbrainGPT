/* eslint-disable max-lines */
import { useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useRecommendModal = () => {
  const [isRecommendModalOpen, setIsRecommendModalOpen] = useState(false);

  return {
    isRecommendModalOpen,
    setIsRecommendModalOpen,
  };
};
