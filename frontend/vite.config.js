import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()], // 這裡就是關鍵：掛載 Vue 插件
  resolve: {
    alias: {
      // 設定 @ 符號指向 src 目錄，方便組件引入
      '@': path.resolve(__dirname, './src'),
    },
  },
})