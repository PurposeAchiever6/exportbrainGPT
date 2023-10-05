import { Answer } from "@/lib/context/BrainProvider/types";
import { useAxios } from "@/lib/hooks";

import {
  addBrainSubscriptions,
  createBrain,
  deleteBrain,
  endPersonalTest,
  getBrain,
  getBrainDocuments,
  getBrains,
  getBrainsFromChat,
  getBrainUsers,
  getDefaultBrain,
  getLinkedinScraping,
  getQuestions,
  setAsDefaultBrain,
  Subscription,
  updateBrain,
  updateBrainAccess,
} from "./brain";
import {
  CreateBrainInput,
  SubscriptionUpdatableProperties,
  UpdateBrainInput,
} from "./types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainApi = () => {
  const { axiosInstance } = useAxios();

  return {
    getBrainDocuments: async (brainId: string) =>
      getBrainDocuments(brainId, axiosInstance),
    createBrain: async (brain: CreateBrainInput) =>
      createBrain(brain, axiosInstance),
    deleteBrain: async (id: string) => deleteBrain(id, axiosInstance),
    getDefaultBrain: async () => getDefaultBrain(axiosInstance),
    getBrains: async () => getBrains(axiosInstance),
    getBrain: async (id: string) => getBrain(id, axiosInstance),
    getBrainsFromChat: async (question: string) => getBrainsFromChat(question, axiosInstance),
    getLinkedinScraping: async (id: string) => getLinkedinScraping(id, axiosInstance),
    getQuestions: async (num: number) => getQuestions(num, axiosInstance),
    endPersonalTest: async (answers: Answer[]) =>
      endPersonalTest(answers, axiosInstance),
    addBrainSubscriptions: async (
      brainId: string,
      subscriptions: Subscription[]
    ) => addBrainSubscriptions(brainId, subscriptions, axiosInstance),
    getBrainUsers: async (brainId: string) =>
      getBrainUsers(brainId, axiosInstance),
    updateBrainAccess: async (
      brainId: string,
      userEmail: string,
      subscription: SubscriptionUpdatableProperties
    ) => updateBrainAccess(brainId, userEmail, subscription, axiosInstance),
    setAsDefaultBrain: async (brainId: string) =>
      setAsDefaultBrain(brainId, axiosInstance),
    updateBrain: async (brainId: string, brain: UpdateBrainInput) =>
      updateBrain(brainId, brain, axiosInstance),
  };
};
