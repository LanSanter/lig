# Island Light Generator 專案架構

## 1. 架構原則
- 依據規劃文件採用「輸入判斷 → 情境補完 → 安全過濾」的路徑流程。
- 後端以分層設計：`api`（輸入輸出）、`services`（商業邏輯）、`schemas`（資料契約）。
- 前端採 Vue 3 Composition API，使用狀態機管理 `init -> selection -> result`。


## 2. Backend 分層
- `backend/main.py`：FastAPI app 與路由掛載。
- `backend/api/`：
  - `routes_scenario.py`：判斷輸入是否足夠，回傳直接生成或候選情境。
  - `routes_generate.py`：執行生成流程並回傳結果。
  - `routes_health.py`：健康檢查。
- `backend/services/`：
  - `input_router.py`：`route_input`。
  - `scenario_expander.py`：產出 3~5 選項（。
  - `sample_loader.py`：載入 `backend/data/oneshot_samples.json` one-shot 樣本。
  - `draft_generator.py`：依使用者輸入與 one-shot 匹配結果動態生成文字與 warnings。
- `backend/schemas/`：`InputProfile`, `ScenarioOption`, `GenerationPlan`, `GenerationResult`。

## 3. Frontend 模組
- `src/App.vue`：頁面容器與主視覺。
- `src/components/GenerateForm.vue`：輸入區、主按鈕、流程轉換。
- `src/components/ScenarioSelector.vue`：不足資訊時的方案選擇。
- `src/components/ResultViewer.vue`：結果展示、安全警示、草稿比較（預留）。

## 4. 互動流程（State Machine）
1. `init`：輸入文本與模型設定。
2. 呼叫 `/api/scenario`：
   - `direct_generate`：直接進入生成。
   - `ask_user_to_choose`：顯示情境卡。
3. `selection`：使用者選擇情境並觸發 `/api/generate`。
4. `result`：顯示生成文、score、trigger、warnings。


## 5. One-shot Sample 資料
- 檔案：`backend/data/oneshot_samples.json`
- 載入方法：`backend/services/sample_loader.py` 的 `load_oneshot_samples()`（記憶體快取）。
- 用途：提供 `scenario_expander` 與 `draft_generator` 在不同輸入下產生可變輸出，而非固定回傳。
