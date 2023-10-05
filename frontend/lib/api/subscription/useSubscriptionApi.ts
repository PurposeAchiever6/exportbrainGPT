import { UUID } from "crypto";

import { useAxios } from "@/lib/hooks";

import {
  acceptInvitation,
  declineInvitation,
  getInvitation,
} from "./subscription";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSubscriptionApi = () => {
  const { axiosInstance } = useAxios();

  return {
    acceptInvitation: async (brainId: UUID) =>
      acceptInvitation(brainId, axiosInstance),
    declineInvitation: async (brainId: UUID) =>
      declineInvitation(brainId, axiosInstance),
    getInvitation: async (brainId: UUID) =>
      getInvitation(brainId, axiosInstance),
  };
};
