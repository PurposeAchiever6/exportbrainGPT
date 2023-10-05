"use client";
import Link from "next/link";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";
import PageHeading from "@/lib/components/ui/PageHeading";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

const requiredRolesForUpload: BrainRoleType[] = ["Editor", "Owner"];

const UploadPage = (): JSX.Element => {
  const { getLinkedinScraping } = useBrainApi();
  const { currentBrain } = useBrainContext();
  const { session } = useSupabase();
  const { publish } = useToast();

  if (session === null) {
    redirectToLogin();
  }

  if (currentBrain === undefined) {
    return (
      <div className="flex justify-center items-center mt-5">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md">
          <strong className="font-bold mr-1">Oh no!</strong>
          <span className="block sm:inline">
            {"You need to select a brain first. 🧠💡🥲"}
          </span>
        </div>
      </div>
    );
  }

  const hasUploadRights = requiredRolesForUpload.includes(currentBrain.role);

  if (!hasUploadRights) {
    return (
      <div className="flex justify-center items-center mt-5">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md">
          <strong className="font-bold mr-1">Oh no!</strong>
          <span className="block sm:inline">
            {
              "You don't have the necessary role to upload content to the selected brain. 🧠💡🥲"
            }
          </span>
        </div>
      </div>
    );
  }

  const linkedinScraping = async () => {
    // @ts-ignore : I'm ignoring this because of some specific reason.
    await getLinkedinScraping(currentBrain.id).then((data) => {
      if (data !== "") {
        publish({
          variant: "success",
          text: data,
        });
      }
    });
  };

  return (
    <main className="pt-10">
      <div className="flex flex-col items-center justify-center gap-5">
      <Button
      // eslint-disable-next-line @typescript-eslint/no-misused-promises
        onClick={() => linkedinScraping()}
      >
        Linkedin Scraping
      </Button>
      </div>
      <br />
      <PageHeading
        title={`Upload Knowledge to ${currentBrain.name}`}
        subtitle="Text, document, spreadsheet, presentation, audio, video, and URLs supported"
      />
      <FileUploader />
      <Divider text="or" className="m-5" />
      <Crawler />
      <div className="flex flex-col items-center justify-center gap-5 mt-5">
        <Link href={"/chat"}>
          <Button variant={"secondary"} className="py-3">
            Chat
          </Button>
        </Link>
      </div>
    </main>
  );
};

export default UploadPage;
