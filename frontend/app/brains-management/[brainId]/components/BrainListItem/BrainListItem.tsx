import Link from "next/link";
import { FaBrain } from "react-icons/fa";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { cn } from "@/lib/utils";

import { useBrainListItem } from "./hooks/useBrainListItem";

interface BrainsListItemProps {
  brain: MinimalBrainForUser;
}

export const BrainListItem = ({ brain }: BrainsListItemProps): JSX.Element => {
  const { selected } = useBrainListItem(brain);

  return (
    <div
      className={cn(
        "w-full min-w-48 border-b border-black/10 dark:border-white/25 last:border-none relative group flex overflow-x-hidden hover:bg-gray-100 dark:hover:bg-gray-800",
        selected
          ? "bg-gray-100 dark:bg-gray-800 text-primary dark:text-white"
          : ""
      )}
      data-testid="brains
      -list-item"
    >
      <Link
        className="flex flex-col flex-1 min-w-0 p-4"
        href={`/brains-management/${brain.id}`}
        key={brain.id}
      >
        <div className="flex items-center gap-2">
          <FaBrain className="text-xl" />
          <p>{brain.name}</p>
        </div>
      </Link>

      <div
        aria-hidden
        className="not-sr-only absolute left-1/2 top-0 bottom-0 right-0 bg-gradient-to-r from-transparent to-white dark:to-black pointer-events-none"
      ></div>
    </div>
  );
};
