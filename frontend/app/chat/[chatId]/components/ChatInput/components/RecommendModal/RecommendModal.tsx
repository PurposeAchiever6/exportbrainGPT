/* eslint-disable max-lines */
import { useEffect, useState } from "react";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";
import { BrainResult } from "@/lib/context/BrainProvider/types";

import { useRecommendModal } from "./hooks/useRecommendModal";

interface props {
  message: string
}

export const RecommendModal = ({
  message
}: props): JSX.Element => {
  
  const [recommendBrains, setRecommendBrains] = useState<BrainResult[]>([]);

  const { getBrainsFromChat } = useBrainApi();
  
  const {
    isRecommendModalOpen,
    setIsRecommendModalOpen,
  } = useRecommendModal();

  useEffect(() => {
    const fetchBrains = async () => {
      if (isRecommendModalOpen && message !== "") {
        try {
          const data = await getBrainsFromChat(message);
          setRecommendBrains(data);
        } catch (error) {
          console.error("Error fetching documents", error);
        }
      }     
    }
  
    void fetchBrains(); // "void" tells ESLint that potential promise rejection is intentionally not handled
  }, [isRecommendModalOpen]);
  
  return (
    <Modal
      Trigger={
        <Button
          className="px-3 py-2 sm:px-4 sm:py-2"
          variant={"tertiary"}
          data-testid="recommend-button"
        >
          Recommend
        </Button>
      }
      title="Recommeded Experts"
      desc=""
      isOpen={isRecommendModalOpen}
      setOpen={setIsRecommendModalOpen}
      CloseTrigger={<div />}
    >
      
    <>
      {
        recommendBrains.map((recommendBrain, index) => (
          <div className="flex justify-between" key={index}>
            <p>{recommendBrain.name}</p>
            <p>{recommendBrain.score}</p>
          </div>
        ))
      }
    </>
    </Modal>
  );
};
