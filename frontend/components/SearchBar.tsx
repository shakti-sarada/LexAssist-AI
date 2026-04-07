"use client";

import { motion } from "framer-motion";

export default function SearchBar({
  onOpen,
  dark,
}: {
  onOpen: () => void;
  dark: boolean;
}) {
  return (
    <motion.button
      onClick={onOpen}
      initial={{ opacity: 0, scale: 0.7, rotate: -8 }}
      animate={{
        opacity: 1,
        scale: [1, 1.08, 1],
        rotate: [0, -4, 4, 0],
      }}
      transition={{
        opacity: { duration: 0.4 },
        scale: {
          duration: 1.8,
          repeat: Infinity,
          repeatType: "loop",
          ease: "easeInOut",
        },
        rotate: {
          duration: 1.8,
          repeat: Infinity,
          repeatType: "loop",
          ease: "easeInOut",
        },
      }}
      whileHover={{ scale: 1.12 }}
      whileTap={{ scale: 0.92 }}
      className={`group relative flex items-center justify-center rounded-full shadow-2xl ${
        dark ? "bg-gray-800" : "bg-white"
      } w-24 h-24 border ${dark ? "border-gray-700" : "border-gray-200"}`}
    >
      <motion.div
        animate={{
          boxShadow: dark
            ? [
                "0 0 0px rgba(59,130,246,0.0)",
                "0 0 30px rgba(59,130,246,0.35)",
                "0 0 0px rgba(59,130,246,0.0)",
              ]
            : [
                "0 0 0px rgba(59,130,246,0.0)",
                "0 0 30px rgba(59,130,246,0.25)",
                "0 0 0px rgba(59,130,246,0.0)",
              ],
        }}
        transition={{
          duration: 1.8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute inset-0 rounded-full"
      />

      <motion.div
        initial={{ y: 0 }}
        animate={{ y: [0, -4, 0] }}
        transition={{ duration: 1.4, repeat: Infinity, ease: "easeInOut" }}
        className="relative"
      >
        <svg
          width="42"
          height="42"
          viewBox="0 0 24 24"
          fill="none"
          className="text-blue-500"
        >
          <motion.path
            d="M8 10H16M8 14H13M21 12C21 16.4183 16.9706 20 12 20C10.5306 20 9.14334 19.6872 7.92963 19.1329L4 20L5.02236 16.9343C3.7641 15.5505 3 13.8476 3 12C3 7.58172 7.02944 4 12 4C16.9706 4 21 7.58172 21 12Z"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            initial={{ pathLength: 0, opacity: 0.5 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 1.1, ease: "easeInOut" }}
          />
        </svg>
      </motion.div>

      <div className="absolute -bottom-12 text-center">
        <p
          className={`text-sm font-medium ${
            dark ? "text-gray-300" : "text-gray-600"
          }`}
        >
          Open Chat
        </p>
      </div>
    </motion.button>
  );
}