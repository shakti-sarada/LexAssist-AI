"use client";

import { motion } from "framer-motion";

type Message = {
  role: "user" | "bot";
  text: string;
};

type Chat = {
  id: number;
  messages: Message[];
};

export default function Sidebar({
  dark,
  setDark,
  chats,
  activeChatId,
  setActiveChatId,
  createNewChat,
}: {
  dark: boolean;
  setDark: React.Dispatch<React.SetStateAction<boolean>>;
  chats: Chat[];
  activeChatId: number;
  setActiveChatId: (id: number) => void;
  createNewChat: () => void;
}) {
  return (
    <div className="w-64 bg-gradient-to-b from-gray-900 to-gray-800 text-white p-5 flex flex-col shadow-xl">

      <h2 className="text-xl font-bold mb-4">⚖️ Legal AI</h2>

      {/* NEW CHAT */}
      <button
        onClick={createNewChat}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg mb-4"
      >
        + New Chat
      </button>

      {/* CHAT HISTORY */}
      <div className="flex-1 overflow-y-auto space-y-2">
        {chats.map((chat) => (
          <motion.div
            key={chat.id}
            onClick={() => setActiveChatId(chat.id)}
            className={`p-3 rounded-lg cursor-pointer ${
              chat.id === activeChatId
                ? "bg-blue-500"
                : "hover:bg-gray-700"
            }`}
          >
            Chat {chat.id.toString().slice(-4)}
          </motion.div>
        ))}
      </div>

    </div>
  );
}