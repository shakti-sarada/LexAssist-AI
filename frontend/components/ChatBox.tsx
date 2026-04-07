"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import InputBar from "@/components/InputBar";
import MessageBubble from "@/components/MessageBubble";

type Message = {
  role: "user" | "bot";
  text: string;
};

export default function ChatBox({
  dark,
  open,
  messages,
  setMessages,
  domain,
}: {
  dark: boolean;
  open: boolean;
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  domain: string;
}) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className={`flex-1 flex flex-col h-full ${
            dark ? "bg-gray-900 text-white" : "bg-white text-black"
          }`}
        >

          <div className="p-3 text-sm opacity-70">
            Domain: {domain.toUpperCase()}
          </div>

           <div
            className={`mx-4 mt-2 px-4 py-2 rounded-lg text-xs leading-relaxed border ${
              dark
                ? "bg-yellow-900/40 text-yellow-300 border-yellow-700"
                : "bg-yellow-100 text-yellow-800 border-yellow-300"
            }`}
          >
            ⚠️ This assistant provides information based on government legal
            sources. It is not a substitute for professional legal advice. For
            real cases, please consult a qualified lawyer.
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, i) => (
              <MessageBubble
                key={i}
                role={msg.role}
                text={msg.text}
                dark={dark}
              />
            ))}
            <div ref={bottomRef} />
          </div>

          <div className="p-4">
            <InputBar
              setMessages={setMessages}
              dark={dark}
              domain={domain}
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}