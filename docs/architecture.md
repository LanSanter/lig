# Island Light Generator 專案架構

## 1. 架構原則
- 依據規劃文件採用「輸入判斷 → 情境補完/直出生成 → 安全過濾」的雙路徑流程。
- 後端以分層設計：`api`（輸入輸出）、`services`（商業邏輯）、`schemas`（資料契約）。
- 前端採 Vue 3 Composition API，使用狀態機管理 `init -> selection -> result`。
- API Token 僅存在前端記憶體狀態，不寫入 localStorage 與後端持久層。

## 2. Backend 分層
- `backend/main.py`：FastAPI app 與路由掛載。
- `backend/api/`：
  - `routes_scenario.py`：判斷輸入是否足夠，回傳直接生成或候選情境。
  - `routes_generate.py`：執行生成流程並回傳結果。
  - `routes_health.py`：健康檢查。
- `backend/services/`：
  - `input_router.py`：`compute_sufficiency` + `route_input`。
  - `scenario_expander.py`：資訊不足時產出 3~5 選項（目前實作為 2 筆示例）。
  - `draft_generator.py`：範例生成結果與 trigger metadata。
- `backend/schemas/`：`InputProfile`, `ScenarioOption`, `GenerationPlan`, `GenerationResult`。

## 3. Frontend 模組
- `src/App.vue`：頁面容器與主視覺。
- `src/components/TokenInput.vue`：token 輸入、顯示/隱藏切換。
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

## 5. 安全與隱私
- Token 僅作為 API 請求參數傳遞，不持久化。
- `banned_patterns.json` 為風險詞預留規則集。
- 結果回傳 `warnings` 陣列，供前端顯示黃色提示標籤。
