"use client";
import { AnimatePresence, motion } from "framer-motion";
import Link from "next/link";

import Button from "@/lib/components/ui/Button";
import Spinner from "@/lib/components/ui/Spinner";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import DocumentItem from "./DocumentItem";
import { useExplore } from "./hooks/useExplore";

const ExplorePage = (): JSX.Element => {
  const { session } = useSupabase();
  const { documents, setDocuments, isPending } = useExplore();
  const { currentBrain } = useBrainContext();
  if (session === null) {
    redirectToLogin();
  }
  if (currentBrain === undefined) {
    return (
      <div className="flex flex-col items-center justify-center mt-10 gap-1">
        <p className="text-center">
          {"You need to select a brain first. 🧠💡🥲"}
        </p>
      </div>
    );
  }

  return (
    <main>
      <section className="w-full outline-none pt-10 flex flex-col gap-5 items-center justify-center p-6">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-3xl font-bold text-center">
            Explore uploaded data in {currentBrain.name}
          </h1>
          <h2 className="opacity-50">
            View or delete stored data used by your brain
          </h2>
        </div>
        {isPending ? (
          <Spinner />
        ) : (
          <motion.div layout className="w-full max-w-xl flex flex-col gap-5">
            {documents.length !== 0 ? (
              <AnimatePresence mode="popLayout">
                {documents.map((document) => (
                  <DocumentItem
                    key={document.name}
                    document={document}
                    setDocuments={setDocuments}
                  />
                ))}
              </AnimatePresence>
            ) : (
              <div className="flex flex-col items-center justify-center mt-10 gap-1">
                <p className="text-center">Oh No, Your Brain is empty.</p>
                <Link href="/upload">
                  <Button>Upload</Button>
                </Link>
              </div>
            )}
          </motion.div>
        )}
      </section>
    </main>
  );
};

export default ExplorePage;
