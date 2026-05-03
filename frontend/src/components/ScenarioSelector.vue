<template>
  <div class="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-700 w-full">
    <div class="p-5 bg-emerald-100 border border-emerald-200 rounded-2xl flex items-center gap-4 shadow-sm">
      <span class="text-3xl">💡</span>
      <p class="text-emerald-900 font-bold text-lg">目前的靈感還能更具體一點，請挑選一個發展方向：</p>
    </div>
    
    <!-- 使用 Grid 並統一高度 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="opt in options" :key="opt.id"
        class="flex flex-col h-full"
      >
        <button 
          @click="toggleSelection(opt.id)"
          :class="[
            'text-left p-6 bg-white border-2 transition-all group relative overflow-hidden rounded-3xl flex-1 flex flex-col h-full min-h-[220px]',
            selectedId === opt.id ? 'border-emerald-500 shadow-xl ring-4 ring-emerald-500/10' : 'border-slate-100 hover:border-emerald-300 shadow-md'
          ]"
        >
          <div class="flex justify-between items-start mb-4">
            <h3 class="font-black text-xl text-slate-800 group-hover:text-emerald-600 transition-colors leading-tight">{{ opt.title }}</h3>
            <span class="text-xs bg-slate-100 px-3 py-1 rounded-full font-black text-slate-500 group-hover:bg-emerald-600 group-hover:text-white shrink-0">#{{ opt.id }}</span>
          </div>
          
          <!-- 讓內容撐開，使底部標籤對齊 -->
          <p class="text-slate-600 text-sm leading-relaxed mb-6 flex-1 line-clamp-4">{{ opt.scene }}</p>
          
          <div class="flex flex-wrap gap-2 mt-auto">
            <span v-for="tag in opt.tone" :key="tag" class="text-[10px] bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full border border-emerald-100 font-bold">
              {{ tag }}
            </span>
          </div>
        </button>

        <!-- 微調區塊 -->
        <transition name="expand">
          <div v-if="selectedId === opt.id" class="mt-4 p-5 bg-white border-2 border-emerald-500 border-dashed rounded-3xl space-y-4 shadow-lg">
            <label class="block text-sm font-black text-emerald-600 uppercase tracking-widest">自定義微調</label>
            <textarea 
              v-model="userRevision" 
              rows="3"
              placeholder="加一點熱血感..."
              class="w-full text-base border-slate-100 rounded-xl focus:ring-emerald-500 focus:border-emerald-500 resize-none p-4 bg-slate-50"
            ></textarea>
            <button 
              @click="confirmSelection(opt)"
              class="w-full py-4 bg-emerald-600 hover:bg-emerald-700 text-white font-black rounded-xl shadow-lg transition-all active:scale-95"
            >
              確認並生成
            </button>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.expand-enter-active, .expand-leave-active { transition: all 0.3s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; transform: translateY(-10px); }
</style>

<script setup>
import { ref } from 'vue';

// 定義從後端傳入的選項[cite: 1]
defineProps({ 
  options: {
    type: Array,
    default: () => []
  } 
});

// 定義要傳回父組件的事件
const emit = defineEmits(['select']);

const selectedId = ref(null); // 當前選中的 ID[cite: 1]
const userRevision = ref(''); // 使用者輸入的修改建議[cite: 1]

// 切換選中狀態
const toggleSelection = (id) => {
  if (selectedId.value === id) {
    selectedId.value = null; // 再次點擊則收合
  } else {
    selectedId.value = id;
    userRevision.value = ''; // 切換選項時清空微調內容
  }
};

// 確認選擇並回傳資料給父組件 (GenerateForm.vue)[cite: 1]
const confirmSelection = (option) => {
  // 將原本的情境描述與使用者的微調進行拼接[cite: 1]
  const finalPrompt = userRevision.value 
    ? `${option.scene} (額外要求：${userRevision.value})`
    : option.scene;


  emit('select', {
    final_prompt: finalPrompt,             // 拼接後的內容
    characters: option.characters,         // 角色清單
    trigger: option.trigger_candidates[0], // 預計使用的觸發梗
    tone: option.tone                      // 風格色調[cite: 1]
  }); // 回傳拼接後的字串[cite: 1]
};
</script>
