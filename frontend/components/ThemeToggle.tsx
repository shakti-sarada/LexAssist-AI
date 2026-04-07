// "use client";
//
// import { motion } from "framer-motion";
//
// export default function ThemeToggle({
//   dark,
//   setDark,
// }: {
//   dark: boolean;
//   setDark: React.Dispatch<React.SetStateAction<boolean>>;
// }) {
//   return (
//     <motion.button
//       onClick={() => setDark(!dark)}
//       whileTap={{ scale: 0.85 }}
//       className={`fixed top-4 right-4 z-50 p-3 rounded-full shadow-xl backdrop-blur-md ${
//         dark ? "bg-gray-800 text-yellow-300" : "bg-white text-gray-800"
//       }`}
//     >
//       <motion.div
//         key={dark ? "moon" : "sun"}
//         initial={{ rotate: -90, scale: 0 }}
//         animate={{ rotate: 0, scale: 1 }}
//         exit={{ rotate: 90, scale: 0 }}
//         transition={{ duration: 0.3 }}
//         className="text-xl"
//       >
//         {dark ? "🌙" : "☀️"}
//       </motion.div>
//     </motion.button>
//   );
// }

"use client";

import { motion } from "framer-motion";

export default function ThemeToggle({
  dark,
  setDark,
  domain,
  setDomain,
}: {
  dark: boolean;
  setDark: React.Dispatch<React.SetStateAction<boolean>>;
  domain: string;
  setDomain: React.Dispatch<React.SetStateAction<string>>;
}) {
  return (
    <div className="fixed top-4 right-4 z-50 flex items-center gap-3 backdrop-blur-lg bg-white/10 border border-white/10 px-3 py-2 rounded-xl shadow-xl">

      {/* 🌐 DOMAIN SELECTOR */}
      <div className="flex gap-1">
        {["consumer", "food", "cyber"].map((d) => (
          <motion.button
            key={d}
            onClick={() => setDomain(d)}
            whileTap={{ scale: 0.9 }}
            whileHover={{ scale: 1.05 }}
            className={`px-3 py-1 text-sm rounded-lg transition-all ${
              domain === d
                ? "bg-blue-600 text-white shadow-md"
                : dark
                ? "text-gray-300 hover:bg-gray-700"
                : "text-gray-700 hover:bg-gray-200"
            }`}
          >
            {d.charAt(0).toUpperCase() + d.slice(1)}
          </motion.button>
        ))}
      </div>

      {/* 🌙 THEME TOGGLE */}
      <motion.button
        onClick={() => setDark(!dark)}
        whileTap={{ scale: 0.85 }}
        className={`p-2 rounded-full shadow-md ${
          dark ? "bg-gray-800 text-yellow-300" : "bg-white text-gray-800"
        }`}
      >
        <motion.div
          key={dark ? "moon" : "sun"}
          initial={{ rotate: -90, scale: 0 }}
          animate={{ rotate: 0, scale: 1 }}
          exit={{ rotate: 90, scale: 0 }}
          transition={{ duration: 0.3 }}
          className="text-lg"
        >
          {dark ? "🌙" : "☀️"}
        </motion.div>
      </motion.button>
    </div>
  );
}