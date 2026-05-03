<template>
  <!-- min-h-screen 確保背景色填滿整個螢幕 -->
  <!-- bg-emerald-50 是淺綠色背景 -->
  <div class="min-h-screen bg-emerald-50 py-12 px-4 md:px-8">
    
    <!-- mx-auto 搭配 max-w-4xl 是置中的關鍵 -->
    <header class="max-w-4xl mx-auto mb-12 text-center">
      <h1 class="text-5xl font-black mb-4 text-slate-900 tracking-tight">
        Island Light <span class="text-emerald-600">Copypasta</span>
      </h1>
      <p class="text-slate-600 text-lg">將平凡瞬間，昇華為台灣精神的文字藝術</p>
    </header>

    <main class="max-w-4xl mx-auto">
      <GenerateForm />
    </main>
  </div>
</template>

<script setup>
import GenerateForm from './components/GenerateForm.vue'
</script>
