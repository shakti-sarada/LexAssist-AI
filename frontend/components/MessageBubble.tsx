"use client";

import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

type Props = {
  role: "user" | "bot";
  text: string;
  dark: boolean;
};

export default function MessageBubble({ role, text, dark }: Props) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`px-4 py-3 rounded-2xl max-w-lg shadow-md leading-relaxed text-sm ${
          isUser
            ? "bg-blue-600 text-white rounded-br-none"
            : dark
            ? "bg-gray-700 text-white rounded-bl-none"
            : "bg-gray-100 text-black rounded-bl-none"
        }`}
      >
        {isUser ? (
          text
        ) : (
          <ReactMarkdown
            components={{

              strong: ({ children }) => (
                <span className="font-semibold block mt-3 mb-1 text-base">
                  {children}
                </span>
              ),


              p: ({ children }) => (
                <div className="mb-2">{children}</div>
              ),


              ul: ({ children }) => (
                <ul className="list-disc pl-5 mb-2">{children}</ul>
              ),

              li: ({ children }) => (
                <li className="mb-1">{children}</li>
              ),


              br: () => <div className="h-2" />,
            }}
          >
            {text}
          </ReactMarkdown>
        )}
      </div>
    </motion.div>
  );
}