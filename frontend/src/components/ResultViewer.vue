<template>
  <!-- 置中對齊的結果容器 -->
  <section class="w-full bg-slate-900 text-white p-10 md:p-16 rounded-[40px] shadow-[0_35px_60px_-15px_rgba(0,0,0,0.3)] relative overflow-hidden animate-in slide-in-from-bottom-12 duration-1000">
    <!-- 背景裝飾 -->
    <div class="absolute top-0 right-0 p-8 opacity-10 font-black text-9xl pointer-events-none select-none">TAIWAN</div>

    <div class="relative z-10 max-w-3xl mx-auto flex flex-col items-center text-center">
      <!-- 狀態列 -->
      <div class="flex flex-wrap justify-center items-center gap-4 mb-10">
        <span class="px-5 py-2 bg-emerald-400 text-slate-900 rounded-full text-sm font-black uppercase tracking-widest shadow-lg">
          Meme Score: {{ (score * 100).toFixed(0) }}
        </span>
        <div v-if="warnings.length > 0" class="flex items-center gap-2 text-rose-400 text-sm font-bold bg-rose-400/10 px-5 py-2 rounded-full border border-rose-400/20 shadow-sm">
          ⚠️ {{ warnings[0] }}
        </div>
      </div>

      <!-- 主文字區 (置中顯示) -->
      <div class="text-2xl md:text-3xl leading-snug whitespace-pre-wrap font-serif mb-12 text-slate-50 font-medium tracking-wide">
        「{{ text }}」
      </div>

      <!-- 詳細資訊與操作 -->
      <div class="w-full grid grid-cols-1 md:grid-cols-2 gap-10 border-t border-slate-800 pt-10 mt-6 text-left">
        <div class="flex flex-col justify-center">
          <p class="text-xs text-slate-500 uppercase tracking-[0.2em] mb-3 font-bold">Trigger Analysis</p>
          <p class="text-lg mb-2">
            <span class="text-emerald-400 font-black">{{ trigger.source }}</span>
            <span class="mx-3 text-slate-600">→</span>
            <span class="text-emerald-300 font-black">{{ trigger.misheard_as }}</span>
          </p>
          <p class="text-sm text-slate-400 italic leading-relaxed">{{ trigger.explanation }}</p>
        </div>
        <div class="flex items-center justify-center md:justify-end">
          <button @click="copyText" class="w-full md:w-auto px-10 py-5 bg-white text-slate-900 rounded-2xl font-black text-lg hover:bg-emerald-400 transition-all active:scale-90 shadow-2xl hover:shadow-emerald-500/20">
            {{ copied ? '✅ 已存入剪貼簿' : '複製這份感動' }}
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
