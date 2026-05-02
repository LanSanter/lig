<template>
  <section class="bg-slate-900 text-white p-8 rounded-3xl shadow-2xl relative overflow-hidden animate-in zoom-in-95 duration-700">
    <!-- 背景裝飾 -->
    <div class="absolute top-0 right-0 p-4 opacity-5 font-black text-8xl pointer-events-none">TW</div>

    <div class="relative z-10">
      <!-- 狀態列 -->
      <div class="flex flex-wrap items-center gap-3 mb-6">
        <span class="px-3 py-1 bg-yellow-400 text-slate-900 rounded-full text-xs font-bold uppercase tracking-widest">
          Meme Scored: {{ (score * 100).toFixed(0) }}
        </span>
        <div v-if="warnings.length > 0" class="flex items-center gap-1 text-red-400 text-xs font-bold bg-red-400/10 px-3 py-1 rounded-full border border-red-400/20">
          ⚠️ {{ warnings[0] }}
        </div>
      </div>

      <!-- 主文字區 -->
      <div class="text-xl md:text-2xl leading-relaxed whitespace-pre-wrap font-serif mb-10 text-slate-100">
        {{ text }}
      </div>

      <!-- 詳細資訊 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-t border-slate-800 pt-8">
        <div>
          <p class="text-xs text-slate-500 uppercase tracking-widest mb-1">Trigger Analysis</p>
          <p class="text-sm">
            <span class="text-blue-400 font-bold">{{ trigger.source }}</span>
            <span class="mx-2 text-slate-600">→</span>
            <span class="text-yellow-400 font-bold">{{ trigger.misheard_as }}</span>
          </p>
          <p class="text-xs text-slate-400 mt-1 italic leading-tight">{{ trigger.explanation }}</p>
        </div>
        <div class="flex items-end justify-end gap-3">
          <button @click="copyText" class="px-6 py-3 bg-white text-slate-900 rounded-xl font-bold hover:bg-yellow-400 transition-all active:scale-95 shadow-lg">
            {{ copied ? '成功複製！' : '複製複製文' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps({
  text: String,
  score: Number,
  trigger: Object, // TriggerCandidate
  warnings: Array
});

const copied = ref(false);
const copyText = () => {
  navigator.clipboard.writeText(props.text);
  copied.value = true;
  setTimeout(() => copied.value = false, 2000);
};
</script>
