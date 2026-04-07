"use client";

import { useState } from "react";

type Message = {
  role: "user" | "bot";
  text: string;
};

export default function InputBar({
  setMessages,
  dark,
  domain,
}: {
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  dark: boolean;
  domain: string;
}) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userMessage },
      { role: "bot", text: "..." },
    ]);

    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          domain: domain,
        }),
      });

      const data = await res.json();

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "bot",
          text: data.response,
        };
        return updated;
      });

    } catch (err) {
      console.error(err);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "bot",
          text: "Error connecting to server ❌",
        };
        return updated;
      });
    }

    setLoading(false);
  };

  return (
    <div
      className={`flex gap-2 p-2 rounded-xl shadow ${
        dark ? "bg-gray-800" : "bg-gray-100"
      }`}
    >
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        disabled={loading}
        className="flex-1 p-3 rounded-lg outline-none bg-transparent"
        placeholder={loading ? "Waiting..." : "Ask something..."}
      />

      <button
        onClick={handleSend}
        disabled={loading}
        className={`px-4 rounded-lg text-white ${
          loading
            ? "bg-gray-500"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "..." : "➤"}
      </button>
    </div>
  );
}