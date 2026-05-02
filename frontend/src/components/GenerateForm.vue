<template>
  <div class="space-y-8">
    <!-- 0. 健康檢查狀態 (非必要，但建議) -->
    <div v-if="serverStatus === 'error'" class="p-4 bg-red-100 text-red-700 rounded-xl text-center font-bold">
      伺服器連線失敗，請稍後再試。
    </div>

    <!-- 1. 輸入區 -->
    <section class="bg-white p-6 rounded-2xl shadow-md border-t-4 border-blue-500">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-bold text-slate-800">輸入你的靈感</h2>
        <div v-if="loading" class="flex items-center gap-2 text-blue-500 text-sm font-bold">
          <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          處理中...
        </div>
      </div>
      
      <textarea 
        v-model="form.user_input" 
        rows="4" 
        placeholder="例如：昨天在 Google Store 問店員 Pixel 用什麼處理器..."
        class="w-full rounded-xl border-slate-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all p-4 resize-none"
        :disabled="loading"
      ></textarea>

      <button 
        @click="startProcess"
        :disabled="loading || !form.user_input || !form.api_token"
        class="w-full mt-4 py-4 bg-slate-900 hover:bg-blue-700 disabled:bg-slate-300 text-white font-bold rounded-xl transition-all shadow-lg active:scale-[0.98]"
      >
        開始生成天光
      </button>
    </section>

    <!-- 2. 情境選擇階段 -->
    <ScenarioSelector 
      v-if="step === 'selection'" 
      :options="scenarioOptions" 
      @select="handleScenarioSelect" 
    />

    <!-- 3. 結果展示階段 -->
    <ResultViewer 
      v-if="step === 'result' && result" 
      v-bind="result"
      :trigger="result.trigger_used"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import ScenarioSelector from './ScenarioSelector.vue';
import ResultViewer from './ResultViewer.vue';

const API_BASE = '/api';
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
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error();
  } catch (e) {
    serverStatus.value = 'error';
  }
});

// 第一階段：判斷充分性
const startProcess = async () => {
  loading.value = true;
  step.value = 'init';
  
  try {
    const res = await fetch(`${API_BASE}/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_input: form.user_input })
    });
    const data = await res.json();

    scenarioOptions.value = data.options;
    step.value = 'selection';
  } catch (e) {
    alert('API 呼叫失敗，請檢查後端服務');
  } finally {
    loading.value = false;
  }
};

// 第二階段：處理情境選擇後生成
const handleScenarioSelect = async (opt) => {
  loading.value = true;
  // 拼接情境描述以利生成更精準的結果
  const enrichedInput = `${opt.scene} (Trigger: ${opt.trigger_candidates[0]})`;
  await finalizeGeneration(enrichedInput);
  loading.value = false;
};

// 最終生成邏輯
const finalizeGeneration = async (input) => {
  try {
    const res = await fetch(`${API_BASE}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_input: input
      })
    });
    result.value = await res.json();
    step.value = 'result';
  } catch (e) {
    alert('生成失敗');
  }
};
</script>
