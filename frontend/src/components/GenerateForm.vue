<template>
  <div class="space-y-10 w-full flex flex-col items-center">
    <!-- 健康檢查狀態 -->
    <div v-if="serverStatus === 'error'" class="w-full p-4 bg-red-100 text-red-700 rounded-xl text-center font-bold shadow-sm">
      伺服器連線失敗，請稍後再試。
    </div>

    <!-- 1. 輸入區：置中並放大 -->
    <section class="w-full bg-white p-10 rounded-3xl shadow-xl border-t-8 border-emerald-500 transition-all">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-extrabold text-slate-800 tracking-wide">輸入你的靈感</h2>
        <div v-if="loading" class="flex items-center gap-3 text-emerald-600 font-bold">
          <svg class="animate-spin h-6 w-6" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-lg">醞釀中...</span>
        </div>
      </div>
      
      <!-- 放大後的 TextArea -->
      <textarea 
        v-model="form.user_input" 
        rows="6" 
        placeholder="例如：昨天在 Google Store 問店員 Pixel 用什麼處理器..."
        class="w-full text-xl rounded-2xl border-slate-200 focus:border-emerald-500 focus:ring-8 focus:ring-emerald-500/10 transition-all p-6 resize-none shadow-inner bg-slate-50"
        :disabled="loading"
      ></textarea>

      <button 
        @click="startProcess"
        :disabled="loading || !form.user_input"
        class="w-full mt-8 py-5 bg-slate-900 hover:bg-emerald-700 disabled:bg-slate-300 text-white text-xl font-black rounded-2xl transition-all shadow-2xl active:scale-[0.97] tracking-widest"
      >
        開始生成天光
      </button>
    </section>

    <!-- 2. 情境選擇階段 -->
    <div class="w-full flex justify-center">
        <ScenarioSelector 
          v-if="step === 'selection'" 
          :options="scenarioOptions" 
          @select="handleScenarioSelect" 
          class="w-full"
        />
    </div>

    <!-- 3. 結果展示階段 -->
    <div class="w-full flex justify-center">
        <ResultViewer 
          v-if="step === 'result' && result" 
          v-bind="result"
          :trigger="result.trigger_used"
          class="w-full"
        />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import ScenarioSelector from './ScenarioSelector.vue';
import ResultViewer from './ResultViewer.vue';
import { apiClient } from '../api/client';


const step = ref('init'); // init, selection, result
const loading = ref(false);
const serverStatus = ref('ok');

const form = reactive({
  user_input: ''
});

const scenarioOptions = ref([]);
const result = ref(null);

// 生命週期：啟動時檢查健康狀態[cite: 1]
onMounted(async () => {
  try {
    const res = await apiClient.get(`/health`);
    if (res.status !== 'ok') throw new Error();
  } catch (e) {
    serverStatus.value = 'error';
  }
});

// 第一階段：判斷充分性
const startProcess = async () => {
  loading.value = true;
  step.value = 'init';
  
  try {
    const data = await apiClient.post('/scenario', { 
      user_input: form.user_input 
    });

    scenarioOptions.value = data.options;
    step.value = 'selection';
  } catch (e) {
    alert('API 呼叫失敗，請檢查後端服務');
  } finally {
    loading.value = false;
  }
};

// 第二階段：處理情境選擇後生成
const handleScenarioSelect = async (payload) => {
  loading.value = true;
  
  // payload 包含了從子組件傳回的封裝資訊[cite: 1]
  const { final_prompt, characters, trigger, tone } = payload;
  
  // 將這些資訊傳入最終生成函數
  await finalizeGeneration({
    user_input: final_prompt,
    characters: characters,
    trigger: trigger,
    tone: tone
  });
  
  loading.value = false;
};

// 最終生成邏輯
const finalizeGeneration = async (params) => {
  try {
    const data = await apiClient.post('/generate',params);
    result.value = data;    
    step.value = 'result';
  } catch (e) {
    alert('生成失敗');
  }
};
</script>
