<template>
  <div class="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <!-- 提示標題區 -->
    <div class="p-4 bg-blue-50 border border-blue-100 rounded-xl flex items-center gap-3">
      <span class="text-xl">🤔</span>
      <p class="text-blue-800 text-sm font-medium">目前的靈感還能更具體一點，請挑選一個發展方向：</p>
    </div>
    
    <!-- 情境卡片列表 -->
    <div class="grid gap-4">
      <div 
        v-for="opt in options" :key="opt.id"
        class="flex flex-col"
      >
        <!-- 情境卡片主體 -->
        <button 
          @click="toggleSelection(opt.id)"
          :class="[
            'text-left p-5 bg-white border-2 transition-all group relative overflow-hidden rounded-2xl',
            selectedId === opt.id ? 'border-blue-500 shadow-md ring-2 ring-blue-100' : 'border-slate-100 hover:border-blue-300'
          ]"
        >
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-bold text-lg text-slate-800 group-hover:text-blue-600 transition-colors">{{ opt.title }}</h3>
            <span class="text-[10px] bg-slate-100 px-2 py-1 rounded-md uppercase font-black text-slate-500 group-hover:bg-blue-600 group-hover:text-white">Option {{ opt.id }}</span>
          </div>
          <p class="text-slate-600 text-sm leading-relaxed mb-3">{{ opt.scene }}</p>
          
          <div class="flex flex-wrap gap-2 mb-1">
            <span v-for="tag in opt.tone" :key="tag" class="text-[10px] bg-slate-50 text-slate-500 px-2 py-0.5 rounded border border-slate-100">
              #{{ tag }}
            </span>
          </div>
        </button>

        <!-- 選中後展開的微調區塊 (User Revision) -->
        <transition 
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="transform -translate-y-2 opacity-0"
          enter-to-class="transform translate-y-0 opacity-100"
        >
          <div v-if="selectedId === opt.id" class="mt-2 p-4 bg-white border-2 border-blue-500 border-dashed rounded-2xl space-y-3 mx-2">
            <label class="block text-xs font-bold text-blue-600 uppercase tracking-wider">自定義微調 (選填)</label>
            <textarea 
              v-model="userRevision" 
              rows="2"
              placeholder="例如：加一點爆肝感、讓結局更中二一點...[cite: 1]"
              class="w-full text-sm border-slate-200 rounded-xl focus:ring-blue-500 focus:border-blue-500 resize-none p-3 bg-slate-50"
            ></textarea>
            <button 
              @click="confirmSelection(opt)"
              class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg shadow-blue-200 transition-all active:scale-[0.98]"
            >
              確認並生成複製文
            </button>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

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

  emit('select', finalPrompt); // 回傳拼接後的字串[cite: 1]
};
</script>
