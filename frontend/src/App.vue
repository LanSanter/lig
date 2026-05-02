<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans p-4 md:p-8">
    <header class="max-w-3xl mx-auto mb-10 text-center">
      <h1 class="text-4xl font-black mb-2 text-slate-900 tracking-tight">
        Island Light <span class="text-blue-600">Copypasta</span>
      </h1>
      <p class="text-slate-500">將平凡瞬間，昇華為台灣精神的文字藝術</p>
    </header>
    <main class="max-w-3xl mx-auto space-y-8">
      <GenerateForm />
    </main>
  </div>
</template>

<script setup>
import GenerateForm from './components/GenerateForm.vue'
</script>
