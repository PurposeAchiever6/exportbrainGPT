import { UUID } from "crypto";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import { Document } from "@/lib/types/Document";

import { useBrainProvider } from "./hooks/useBrainProvider";
import { Model } from "../BrainConfigProvider/types";

export type Brain = {
  id: UUID;
  name: string;
  documents?: Document[];
  status?: string;
  model?: Model;
  max_tokens?: number;
  temperature?: number;
  openai_api_key?: string;
  description?: string;
  prompt_id?: string | null;
  linkedin?: string,
  extraversion?: number,
  neuroticism?: number,
  conscientiousness?: number,
};

export type Question = {
  trait: string;
  positive: boolean;
  question: string;
};

export type Answer = Question & {
  answer: number;
};

export type Personality = {
  score: {
    conscientiousness: number,
    extraversion: number,
    neuroticism: number,
    // Include other properties of score if they exist
  },
  description: {
    conscientiousness: string,
    extraversion: string,
    neuroticism: string,
    // Include other properties of score if they exist
  },
};

export type MinimalBrainForUser = {
  id: UUID;
  name: string;
  role: BrainRoleType;
};

export type BrainResult = {
  brain_id: string;
  name: string;
  score: number;
}

//TODO: rename rights to role in Backend and use MinimalBrainForUser instead of BackendMinimalBrainForUser
export type BackendMinimalBrainForUser = Omit<MinimalBrainForUser, "role"> & {
  rights: BrainRoleType;
};

export type BrainContextType = ReturnType<typeof useBrainProvider>;
