/** @type {import('tailwindcss').Config} */
export default {
  // 包含所有會用到 Tailwind 類別的檔案路徑
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // 自訂顏色或擴充主題
    },
  },
  plugins: [],
}