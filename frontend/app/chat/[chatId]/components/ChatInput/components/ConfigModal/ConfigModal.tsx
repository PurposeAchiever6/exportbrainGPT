/* eslint-disable max-lines */
import { MdCheck, MdSettings } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";
import { models } from "@/lib/context/BrainConfigProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";

import { useConfigModal } from "./hooks/useConfigModal";

export const ConfigModal = ({ chatId }: { chatId?: string }): JSX.Element => {
  const {
    handleSubmit,
    isConfigModalOpen,
    setIsConfigModalOpen,
    register,
    temperature,
    maxTokens,
    model,
  } = useConfigModal(chatId);

  if (chatId === undefined) {
    return <div />;
  }

  return (
    <Modal
      Trigger={
        <Button
          className="p-2 sm:px-3"
          variant={"tertiary"}
          data-testid="config-button"
        >
          <MdSettings className="text-lg sm:text-xl lg:text-2xl" />
        </Button>
      }
      title="Chat configuration"
      desc="Adjust your chat settings"
      isOpen={isConfigModalOpen}
      setOpen={setIsConfigModalOpen}
      CloseTrigger={<div />}
    >
      <form
        onSubmit={(e) => {
          void handleSubmit(e);
          setIsConfigModalOpen(false);
        }}
        className="mt-10 flex flex-col items-center gap-2"
      >
        <fieldset className="w-full flex flex-col">
          <label className="flex-1 text-sm" htmlFor="model">
            Model
          </label>
          <select
            id="model"
            {...register("model")}
            className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
          >
            {models.map((availableModel) => (
              <option value={availableModel} key={availableModel}>
                {availableModel}
              </option>
            ))}
          </select>
        </fieldset>

        <fieldset className="w-full flex mt-4">
          <label className="flex-1" htmlFor="temp">
            Temperature: {temperature}
          </label>
          <input
            id="temp"
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={temperature}
            {...register("temperature")}
          />
        </fieldset>
        <fieldset className="w-full flex mt-4">
          <label className="flex-1" htmlFor="tokens">
            Max tokens: {maxTokens}
          </label>
          <input
            type="range"
            min="10"
            max={defineMaxTokens(model ?? "gpt-3.5-turbo-0613")}
            value={maxTokens}
            {...register("maxTokens")}
          />
        </fieldset>

        <Button className="mt-12 self-end" type="submit">
          Save
          <MdCheck className="text-xl" />
        </Button>
      </form>
    </Modal>
  );
};
