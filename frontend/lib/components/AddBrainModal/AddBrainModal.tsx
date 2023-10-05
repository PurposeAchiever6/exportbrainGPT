/* eslint-disable max-lines */
import { useEffect, useState } from "react";
import { MdAdd } from "react-icons/md";

// import { PublicPrompts } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/components/SettingsTab/components/PublicPrompts";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { Modal } from "@/lib/components/ui/Modal";
import { models, paidModels } from "@/lib/context/BrainConfigProvider/types";
import { Personality, Question } from "@/lib/context/BrainProvider/types";
import { defineMaxTokens } from "@/lib/helpers/defineMexTokens";

import { useAddBrainModal } from "./hooks/useAddBrainModal";
// import { Divider } from "../ui/Divider";
import { TextArea } from "../ui/TextArea";

export const AddBrainModal = (): JSX.Element => {
  const {
    handleSubmit,
    isShareModalOpen,
    setIsShareModalOpen,
    register,
    setValue,
    openAiKey,
    temperature,
    maxTokens,
    model,
    isPending,
    // pickPublicPrompt,
  } = useAddBrainModal();

  const [personality, setPersonality] = useState<boolean>(false);
  const [createVisiable, setCreateVisible] = useState<boolean>(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<number[]>([]);
  const { getQuestions, endPersonalTest } = useBrainApi();

  useEffect(() => {
    const fetchDocuments = async (num: number) => {
      try {
        // @ts-ignore : I'm ignoring this because of some specific reason.
        const data = await getQuestions(num);
        // @ts-ignore : I'm ignoring this because of some specific reason.
        setQuestions(data);
        setAnswers(new Array(data?.length).fill(0));
      } catch (error) {
        console.error("Error fetching documents", error);
        setQuestions([]);
      }
    };
    // default num is 2
    void fetchDocuments(2);
  }, []);

  const endTest = async () => {
    await endPersonalTest(
      questions.map((question, index) => ({
        ...question,
        answer: answers[index],
      }))
    ).then((data?: Personality) => {
      if (data) {
        console.log(data.score);
        setCreateVisible(true);
        register("conscientiousness");
        setValue("conscientiousness", data.score.conscientiousness);
        register("extraversion");
        setValue("extraversion", data.score.extraversion);
        register("neuroticism");
        setValue("neuroticism", data.score.neuroticism);
      }
    });
  };

  return (
    <Modal
      Trigger={
        <Button variant={"secondary"}>
          Add New Brain
          <MdAdd className="text-xl" />
        </Button>
      }
      title="Add Brain"
      desc="Create a new brain to start aggregating content"
      isOpen={isShareModalOpen}
      setOpen={setIsShareModalOpen}
      CloseTrigger={<div />}
    >
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void handleSubmit();
        }}
        className="my-10 flex flex-col items-center gap-2"
      >
        <Field
          label="Enter a brain name"
          autoFocus
          placeholder="E.g. History notes"
          autoComplete="off"
          className="flex-1"
          {...register("name")}
        />

        <TextArea
          label="Enter a brain description"
          placeholder="My new brain is about..."
          autoComplete="off"
          className="flex-1 m-3"
          {...register("description")}
        />

        <Field
          label="OpenAI API Key"
          placeholder="sk-xxx"
          autoComplete="off"
          className="flex-1"
          {...register("openAiKey")}
        />

        <fieldset className="w-full flex flex-col">
          <label className="flex-1 text-sm" htmlFor="model">
            Model
          </label>
          <select
            id="model"
            {...register("model")}
            className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
          >
            {(openAiKey !== undefined ? paidModels : models).map(
              (availableModel) => (
                <option value={availableModel} key={availableModel}>
                  {availableModel}
                </option>
              )
            )}
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
            max={defineMaxTokens(model)}
            value={maxTokens}
            {...register("maxTokens")}
          />
        </fieldset>
        <Field
          label="Prompt title"
          placeholder="My awesome prompt name"
          autoComplete="off"
          className="flex-1"
          {...register("prompt.title")}
        />
        <TextArea
          label="Prompt content"
          placeholder="As an AI, your..."
          autoComplete="off"
          className="flex-1"
          {...register("prompt.content")}
        />
        <div className="flex flex-row justify-start w-full mt-4">
          <label className="flex items-center">
            <span className="mr-2 text-gray-700">Set as default brain</span>
            <input
              type="checkbox"
              {...register("setDefault")}
              className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
            />
          </label>
        </div>

        <div className="flex items-center justify-center">
          <hr className="border-t border-gray-300 w-12" />
          <p className="px-3 text-center text-gray-500 dark:text-white">
            Personality
          </p>
          <input
            type="checkbox"
            className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
            onChange={() => setPersonality(!personality)}
          />{" "}
          &nbsp;&nbsp;&nbsp;
          <hr className="border-t border-gray-300 w-12" />
        </div>

        {personality ? (
          <>
            <Field
              label="Enter your linkedin"
              autoFocus
              placeholder="https://www.linkedin.com/in/"
              autoComplete="off"
              className="flex-1"
              {...register("linkedin")}
            />
            {questions.map((question, index) => (
              <>
                <TextArea
                  defaultValue={question.question}
                  readOnly
                  autoComplete="off"
                  className="flex-1"
                  name={index.toString()}
                />
                <div className="flex justify-between w-full">
                  <input
                    type="radio"
                    name={"radio" + index.toString()}
                    value={0}
                    className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
                    onChange={() =>
                      setAnswers([
                        ...answers.slice(0, index),
                        0,
                        ...answers.slice(index + 1),
                      ])
                    }
                  />
                  Totally disagree
                  <input
                    type="radio"
                    name={"radio" + index.toString()}
                    value={1}
                    className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
                    onChange={() =>
                      setAnswers([
                        ...answers.slice(0, index),
                        1,
                        ...answers.slice(index + 1),
                      ])
                    }
                  />
                  disagree
                  <input
                    type="radio"
                    name={"radio" + index.toString()}
                    value={2}
                    className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
                    onChange={() =>
                      setAnswers([
                        ...answers.slice(0, index),
                        2,
                        ...answers.slice(index + 1),
                      ])
                    }
                  />
                  neutral
                  <input
                    type="radio"
                    name={"radio" + index.toString()}
                    value={3}
                    className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
                    onChange={() =>
                      setAnswers([
                        ...answers.slice(0, index),
                        3,
                        ...answers.slice(index + 1),
                      ])
                    }
                  />
                  agree
                  <input
                    type="radio"
                    name={"radio" + index.toString()}
                    value={4}
                    className="form-checkbox h-5 w-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-400"
                    onChange={() =>
                      setAnswers([
                        ...answers.slice(0, index),
                        4,
                        ...answers.slice(index + 1),
                      ])
                    }
                  />
                  Totally agree
                </div>
              </>
            ))}
            <a
              onClick={() => {
                endTest().catch(console.error);
              }}
              style={{ cursor: "pointer" }}
            >
              End Test
            </a>
          </>
        ) : (
          <></>
        )}

        {createVisiable ? (
          <Button
            isLoading={isPending}
            className="mt-12 self-end"
            type="submit"
          >
            Create
            <MdAdd className="text-xl" />
          </Button>
        ) : (
          <></>
        )}
      </form>
    </Modal>
  );
};
