"use client";

import { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import Sidebar from "@/components/Sidebar";
import ChatBox from "@/components/ChatBox";
import SearchBar from "@/components/SearchBar";
import SplashScreen from "@/components/SplashScreen";
import ThemeToggle from "@/components/ThemeToggle";

type Message = {
  role: "user" | "bot";
  text: string;
};

type Chat = {
  id: number;
  messages: Message[];
};

export default function Home() {
  const [dark, setDark] = useState(false);
  const [loading, setLoading] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);

  const [domain, setDomain] = useState("consumer");

  const [chats, setChats] = useState<Chat[]>([
    { id: 1, messages: [{ role: "bot", text: "Hello 👋" }] },
  ]);

  const [activeChatId, setActiveChatId] = useState(1);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2200);
    return () => clearTimeout(timer);
  }, []);

  const activeChat = chats.find((c) => c.id === activeChatId)!;

  const updateMessages: React.Dispatch<
    React.SetStateAction<Message[]>
  > = (value) => {
    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id !== activeChatId) return chat;

        const newMessages =
          typeof value === "function"
            ? value(chat.messages)
            : value;

        return { ...chat, messages: newMessages };
      })
    );
  };

  const createNewChat = () => {
    const newChat: Chat = {
      id: Date.now(),
      messages: [{ role: "bot", text: "New chat started 🚀" }],
    };

    setChats((prev) => [newChat, ...prev]);
    setActiveChatId(newChat.id);
    setChatOpen(true);
  };

  return (
    <>
      <AnimatePresence>
        {loading && <SplashScreen />}
      </AnimatePresence>

      {!loading && (
        <div className="flex h-screen overflow-hidden">
          <Sidebar
            dark={dark}
            setDark={setDark}
            chats={chats}
            activeChatId={activeChatId}
            setActiveChatId={setActiveChatId}
            createNewChat={createNewChat}
          />

          <div className="flex-1 relative">

            {/* ✅ FIXED: pass domain props */}
            <ThemeToggle
              dark={dark}
              setDark={setDark}
              domain={domain}
              setDomain={setDomain}
            />

            {!chatOpen && (
              <div className="absolute inset-0 flex items-center justify-center">
                <SearchBar onOpen={() => setChatOpen(true)} dark={dark} />
              </div>
            )}

            <ChatBox
              dark={dark}
              open={chatOpen}
              messages={activeChat.messages}
              setMessages={updateMessages}
              domain={domain}
            />
          </div>
        </div>
      )}
    </>
  );
}