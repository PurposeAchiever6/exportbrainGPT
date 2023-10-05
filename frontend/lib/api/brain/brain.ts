/* eslint-disable max-lines */
import { AxiosInstance } from "axios";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import {
  BackendMinimalBrainForUser,
  Brain,
  MinimalBrainForUser,
} from "@/lib/context/BrainProvider/types";
import { Document } from "@/lib/types/Document";

import {
  CreateBrainInput,
  SubscriptionUpdatableProperties,
  UpdateBrainInput,
} from "./types";
import { mapBackendMinimalBrainToMinimalBrain } from "./utils/mapBackendMinimalBrainToMinimalBrain";
import {
  BackendSubscription,
  mapSubscriptionToBackendSubscription,
} from "./utils/mapSubscriptionToBackendSubscription";
import { mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties } from "./utils/mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties";

export const getBrainDocuments = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Document[]> => {
  const response = await axiosInstance.get<{ documents: Document[] }>(
    `/explore/?brain_id=${brainId}`
  );

  return response.data.documents;
};

export const createBrain = async (
  brain: CreateBrainInput,
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser> => {
  return mapBackendMinimalBrainToMinimalBrain(
    (await axiosInstance.post<BackendMinimalBrainForUser>(`/brains/`, brain))
      .data
  );
};

export const getBrain = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Brain | undefined> => {
  const brain = (
    await axiosInstance.get<Brain | undefined>(`/brains/${brainId}/`)
  ).data;

  return brain;
};

export const deleteBrain = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/brains/${brainId}/subscription`);
};

export const getDefaultBrain = async (
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser | undefined> => {
  return mapBackendMinimalBrainToMinimalBrain(
    (await axiosInstance.get<BackendMinimalBrainForUser>(`/brains/default/`))
      .data
  );
};

export const getBrains = async (
  axiosInstance: AxiosInstance
): Promise<MinimalBrainForUser[]> => {
  const { brains } = (
    await axiosInstance.get<{ brains: BackendMinimalBrainForUser[] }>(
      `/brains/`
    )
  ).data;

  return brains.map(mapBackendMinimalBrainToMinimalBrain);
};

export type Subscription = { email: string; role: BrainRoleType };

export const addBrainSubscriptions = async (
  brainId: string,
  subscriptions: Subscription[],
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.post(
    `/brains/${brainId}/subscription`,
    subscriptions.map(mapSubscriptionToBackendSubscription)
  );
};

export const getBrainUsers = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<Subscription[]> => {
  const brainsUsers = (
    await axiosInstance.get<BackendSubscription[]>(`/brains/${brainId}/users`)
  ).data;

  return brainsUsers.map((brainUser) => ({
    email: brainUser.email,
    role: brainUser.rights,
  }));
};

export const updateBrainAccess = async (
  brainId: string,
  userEmail: string,
  subscription: SubscriptionUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.put(`/brains/${brainId}/subscription`, {
    ...mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties(
      subscription
    ),
    email: userEmail,
  });
};

export const setAsDefaultBrain = async (
  brainId: string,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.post(`/brains/${brainId}/default`);
};

export const updateBrain = async (
  brainId: string,
  brain: UpdateBrainInput,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.put(`/brains/${brainId}/`, brain);
};
