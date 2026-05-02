# Island Light Copypasta Generator

一個用於將使用者輸入的情境、故事、風格、人物或模糊需求，轉換成「島嶼天光風格複製文」的文字生成系統。

本專案不是單純的模板填空器，而是將任意輸入轉換成以下敘事結構：

```text
普通情境
  → 誤聽 / 諧音 / 語義錯位觸發
  → 現場群體異常反應
  → 荒謬升級
  → 台灣精神式收束
```

---

## 1. 專案目標

本系統的目標是建立一個可互動、可擴充、可部署的迷因複製文生成器。

使用者可以輸入：

```text
1. 具體故事
2. 人物與場景
3. 風格需求
4. 模糊情緒
5. 幾個任意關鍵字
```

系統會先判斷輸入資訊是否足夠。

若資訊足夠，直接分析並生成複製文。

若資訊不足，系統會先產生數個候選情境，讓使用者選擇或修改，再進入生成流程。

---

## 2. 系統總體流程

```text
User Input
  ↓
Input Sufficiency Router
  ├─ 資訊足夠
  │    ↓
  │  Scene Analyzer
  │    ↓
  │  Trigger Miner
  │    ↓
  │  Narrative Planner
  │    ↓
  │  Draft Generator
  │    ↓
  │  Meme Scorer
  │    ↓
  │  Safety Filter
  │    ↓
  │  Output
  │
  └─ 資訊不足
       ↓
     Scenario Expander
       ↓
     回傳 3~5 個情境選項
       ↓
     使用者選擇 / 修改
       ↓
     Scene Analyzer
       ↓
     Trigger Miner
       ↓
     Narrative Planner
       ↓
     Draft Generator
       ↓
     Meme Scorer
       ↓
     Safety Filter
       ↓
     Output
```

---

## 3. 技術選型

建議保留 Python 作為後端主語言。

### 後端

```text
Python 3.11+
FastAPI
Pydantic
Uvicorn / Gunicorn
SQLite / PostgreSQL
```

### 前端

可選：

```text
Vue
React
Svelte
```

### 部署

```text
Nginx
Uvicorn / Gunicorn
systemd 或 Docker
HTTPS
```

---

## 4. 專案目錄建議

```text
island-light-generator/
  README.md
  .env.example
  requirements.txt
  pyproject.toml

  backend/
    main.py
    config.py

    api/
      routes_generate.py
      routes_scenario.py
      routes_health.py

    schemas/
      input_profile.py
      scenario_option.py
      generation_plan.py
      generation_result.py

    services/
      input_router.py
      scene_analyzer.py
      scenario_expander.py
      trigger_miner.py
      narrative_planner.py
      draft_generator.py
      meme_scorer.py
      safety_filter.py
      llm_client.py

    prompts/
      scene_analyzer.md
      scenario_expander.md
      trigger_miner.md
      narrative_planner.md
      draft_generator.md
      meme_scorer.md

    data/
      prompt_examples.json
      banned_patterns.json
      style_rules.json

    tests/
      test_input_router.py
      test_safety_filter.py
      test_scorer.py

  frontend/
    package.json
    src/
      App.vue
      components/
        TokenInput.vue
        ScenarioSelector.vue
        GenerateForm.vue
        ResultViewer.vue
```

---

## 5. 核心資料結構

### 5.1 InputProfile

```python
from pydantic import BaseModel
from typing import Optional

class InputProfile(BaseModel):
    raw_text: str

    location: Optional[str] = None
    characters: list[str] = []
    event: Optional[str] = None
    key_terms: list[str] = []

    tone: list[str] = []
    style: list[str] = []

    trigger_candidates: list[str] = []

    sufficiency_score: float = 0.0
    missing_slots: list[str] = []
```

用途：  
儲存使用者輸入經過初步解析後的結果。

---

### 5.2 ScenarioOption

```python
from pydantic import BaseModel

class ScenarioOption(BaseModel):
    id: str
    title: str
    scene: str
    characters: list[str]
    trigger_candidates: list[str]
    escalation_hint: str
    tone: list[str]
```

用途：  
當使用者輸入過於模糊時，系統產生 3 到 5 個候選情境供使用者選擇。

---

### 5.3 TriggerCandidate

```python
from pydantic import BaseModel

class TriggerCandidate(BaseModel):
    source: str
    misheard_as: str
    explanation: str
    score: float
```

用途：  
描述一組可用於複製文觸發的誤聽、諧音或語義錯位。

---

### 5.4 NarrativePlan

```python
from pydantic import BaseModel

class NarrativePlan(BaseModel):
    setup: str
    trigger: str
    glitch_start: str
    collective_spread: str
    escalation: list[str]
    emotional_turn: str
    ideological_closure: str
```

用途：  
先產生文章骨架，再進入正式草稿生成。

---

### 5.5 GenerationResult

```python
from pydantic import BaseModel

class GenerationResult(BaseModel):
    text: str
    score: float
    trigger_used: TriggerCandidate
    safety_passed: bool
    warnings: list[str] = []
```

用途：  
儲存最終生成結果與品質評分。

---

## 6. Input Sufficiency Router

### 判斷邏輯

不要只看字數。  
要判斷輸入是否包含可生成故事的必要要素。

建議欄位：

```text
location
characters
event
trigger_candidates
tone
```

### 分數設計

```python
def compute_sufficiency(profile: InputProfile) -> float:
    score = 0.0

    if profile.location:
        score += 0.20

    if profile.characters:
        score += 0.20

    if profile.event:
        score += 0.25

    if profile.key_terms or profile.trigger_candidates:
        score += 0.25

    if profile.tone or profile.style:
        score += 0.10

    return score
```

### 路由邏輯

```python
def route_input(user_input: str):
    profile = llm_extract_profile(user_input)
    profile.sufficiency_score = compute_sufficiency(profile)

    if profile.sufficiency_score >= 0.65:
        return {
            "mode": "direct_generate",
            "profile": profile
        }

    options = llm_generate_scenario_options(
        user_input=user_input,
        missing_slots=profile.missing_slots
    )

    return {
        "mode": "ask_user_to_choose",
        "profile": profile,
        "options": options
    }
```

---

## 7. 生成流程虛擬碼

### 7.1 直接生成流程

```python
def generate_meme(user_input: str, api_token: str):
    profile = llm_extract_profile(user_input)

    if compute_sufficiency(profile) < 0.65:
        return ask_user_to_choose_scenario(profile)

    scene = analyze_scene(profile)

    triggers = find_triggers(scene)
    triggers = filter_bad_triggers(triggers)

    plans = []
    for trigger in triggers[:5]:
        plan = make_narrative_plan(scene, trigger)
        plans.append(plan)

    drafts = []
    for plan in plans:
        drafts.extend(generate_drafts(plan, n=2))

    scored_results = []
    for draft in drafts:
        score = score_draft(draft, scene)
        safety = safety_filter(draft)

        if safety.passed:
            scored_results.append({
                "text": draft,
                "score": score,
                "safety": safety
            })

    return max(scored_results, key=lambda x: x["score"])
```

---

### 7.2 模糊輸入補完流程

```python
def ask_user_to_choose_scenario(profile: InputProfile):
    options = scenario_expander(profile)

    return {
        "type": "scenario_selection_required",
        "message": "目前輸入資訊不足，請選擇或修改一個情境方向。",
        "options": options
    }
```

---

### 7.3 使用者選擇後的流程

```python
def handle_user_choice(choice_id: str, previous_state: dict):
    selected = find_option_by_id(
        previous_state["options"],
        choice_id
    )

    profile = normalize_scenario(selected)

    scene = analyze_scene(profile)
    triggers = find_triggers(scene)

    best_trigger = select_best_trigger(triggers)

    plan = make_narrative_plan(scene, best_trigger)

    drafts = generate_drafts(plan, n=5)

    result = select_best_safe_draft(drafts)

    return result
```

---

## 8. Prompt 設計

所有 Prompt 建議存放於：

```text
backend/prompts/
```

---

### 8.1 Scene Analyzer Prompt

檔案：

```text
backend/prompts/scene_analyzer.md
```

內容：

```text
你是一個迷因情境解析器。

請從使用者輸入中抽取以下資訊：

1. location：故事發生地點
2. characters：出現的人物或群體
3. event：主要事件或衝突
4. key_terms：可能被誤聽、諧音轉換或語義扭曲的詞
5. tone：情緒風格
6. style：敘事風格
7. trigger_candidates：可能用於島嶼天光複製文的觸發詞

要求：
- 如果使用者沒有提供某欄位，填 null 或空陣列。
- 不要直接生成複製文。
- 請輸出 JSON。
```

---

### 8.2 Scenario Expander Prompt

檔案：

```text
backend/prompts/scenario_expander.md
```

內容：

```text
你是一個迷因情境補完器。

使用者輸入可能只有風格、情緒、主題，沒有完整事件。
請根據輸入產生 3 到 5 個可用於「島嶼天光風格複製文」的情境選項。

每個選項必須包含：

1. id
2. title
3. scene
4. characters
5. trigger_candidates
6. escalation_hint
7. tone

要求：
- trigger 要能產生誤聽、諧音、台語空耳、英文近音或語義錯位。
- 場景要能自然引出群體合唱。
- 不要直接生成全文。
- 避免真實災難、受害者嘲弄、個資、仇恨或煽動暴力。
- 請輸出 JSON array。
```

---

### 8.3 Trigger Miner Prompt

檔案：

```text
backend/prompts/trigger_miner.md
```

內容：

```text
你是一個中文、台語、英文混合諧音梗分析器。

請根據 scene 和 key_terms 找出可能觸發「島嶼天光風格複製文」的誤聽點。

偏好以下類型：

1. 英文近音中文
2. 中文斷句誤會
3. 台語空耳
4. 情境詞被強行解讀成台灣符號
5. 普通術語被誤會成歌曲起音或 Team Taiwan 口號

每個候選請包含：

- source
- misheard_as
- explanation
- score，範圍 0 到 1

不要生成正文。
請輸出 JSON array。
```

---

### 8.4 Narrative Planner Prompt

檔案：

```text
backend/prompts/narrative_planner.md
```

內容：

```text
你是一個迷因敘事規劃器。

請根據 scene 和 selected_trigger，規劃一篇「島嶼天光風格複製文」的段落骨架。

必須包含：

1. setup：普通開場
2. trigger：誤聽或語義錯位觸發
3. glitch_start：現場突然安靜或異常反應
4. collective_spread：群體同步合唱或同步行為
5. escalation：荒謬升級，至少 2 個
6. emotional_turn：主角情緒崩潰或被感動
7. ideological_closure：台灣精神式結尾

要求：
- 要貼合原本場景，不要硬塞無關元素。
- 不要直接長篇複製任何歌曲歌詞。
- 請輸出 JSON。
```

---

### 8.5 Draft Generator Prompt

檔案：

```text
backend/prompts/draft_generator.md
```

內容：

```text
根據以下 narrative_plan，生成一篇「島嶼天光風格複製文」。

風格要求：

1. 第一人稱敘事
2. 開頭要像真實經歷
3. 觸發點要由誤聽、諧音或語義錯位引出
4. 中段要有現場群體同步反應
5. 後段要荒謬升級
6. 結尾要收束到台灣精神、自由、世界看見台灣、台灣被愛著等情緒
7. 可以誇張，但要維持像網路複製文的口吻

限制：

1. 不要完整複製歌曲歌詞。
2. 不要嘲笑真實受害者。
3. 不要攻擊特定真人。
4. 不要包含個資。
5. 不要煽動暴力。
```

---

### 8.6 Meme Scorer Prompt

檔案：

```text
backend/prompts/meme_scorer.md
```

內容：

```text
你是一個迷因品質評分器。

請根據以下標準評估生成文章：

1. trigger_score：
   誤聽、諧音或語義錯位是否自然。

2. scene_fit_score：
   是否充分利用原本場景元素。

3. escalation_score：
   是否有從小事件擴大到荒謬群體事件。

4. style_score：
   是否符合島嶼天光風格複製文的語氣。

5. novelty_score：
   是否避免過度模板化。

6. safety_score：
   是否避免真實傷害嘲弄、仇恨、個資、暴力煽動與長篇歌詞複製。

請輸出 JSON：

{
  "trigger_score": 0.0,
  "scene_fit_score": 0.0,
  "escalation_score": 0.0,
  "style_score": 0.0,
  "novelty_score": 0.0,
  "safety_score": 0.0,
  "overall_score": 0.0,
  "reason": "..."
}
```

---

## 9. Zero-shot Sample

### Sample 1：資訊足夠

#### User Input

```text
昨天在 Google Store 問店員 Pixel 用什麼處理器，店員說 Tensor，我想改成島嶼天光複製文。
```

#### Scene Analyzer Output

```json
{
  "location": "Google Store",
  "characters": ["我", "店員", "顧客"],
  "event": "詢問 Pixel 手機處理器",
  "key_terms": ["Tensor", "Pixel", "Google Store"],
  "tone": ["荒謬", "感動"],
  "style": ["網路複製文"],
  "trigger_candidates": ["Tensor"]
}
```

#### Trigger Miner Output

```json
[
  {
    "source": "Tensor",
    "misheard_as": "天色",
    "explanation": "Tensor 的開頭音可被強行誤聽為『天色』，能接上島嶼天光式起音。",
    "score": 0.92
  }
]
```

#### Narrative Plan Output

```json
{
  "setup": "主角在 Google Store 詢問 Pixel 規格。",
  "trigger": "店員說 Tensor，被旁邊旅客誤聽成天色。",
  "glitch_start": "整間店突然安靜。",
  "collective_spread": "店員、顧客與觀光客開始同步哼唱。",
  "escalation": [
    "展示機螢幕同時亮起台灣地圖。",
    "手機計算機被拿來打節拍。"
  ],
  "emotional_turn": "主角從困惑變成眼眶泛紅。",
  "ideological_closure": "科技會更新，但台灣精神不會過時。"
}
```

---

### Sample 2：資訊不足

#### User Input

```text
我想要一個很熱血、很荒謬、跟科技有關的島嶼天光複製文。
```

#### Router Output

```json
{
  "mode": "ask_user_to_choose",
  "reason": "輸入只有風格與主題，缺少具體場景、人物與事件。"
}
```

#### Scenario Expander Output

```json
[
  {
    "id": "A",
    "title": "AI 實驗室爆肝型",
    "scene": "大學 AI 實驗室裡，研究生期末前模型訓練失敗，GPU 過熱，外籍交換生誤聽 Tensor error。",
    "characters": ["研究生", "教授", "外籍交換生"],
    "trigger_candidates": ["Tensor error → 天色漸漸光"],
    "escalation_hint": "整棟資工系大樓開始合唱。",
    "tone": ["爆肝", "荒謬", "熱血"]
  },
  {
    "id": "B",
    "title": "半導體無塵室覺醒型",
    "scene": "晶圓廠工程師在無塵室喊 test run，被外國主管誤聽成 Team Taiwan。",
    "characters": ["工程師", "外國主管", "產線人員"],
    "trigger_candidates": ["test run → Team Taiwan"],
    "escalation_hint": "整條產線節拍同步，晶圓良率突然上升。",
    "tone": ["科技島", "國際震撼", "荒謬"]
  },
  {
    "id": "C",
    "title": "機器人展場失控型",
    "scene": "機器人展場中，語音辨識系統把 Team Taiwan 當成啟動指令。",
    "characters": ["主持人", "觀眾", "機器人"],
    "trigger_candidates": ["Team Taiwan → 啟動合唱"],
    "escalation_hint": "全部機器人同步轉向台灣方向敬禮。",
    "tone": ["科幻", "群體同步", "荒謬"]
  }
]
```

---

## 10. Meme Scorer

### 加權公式

```python
def score_draft(scores: dict) -> float:
    return (
        0.25 * scores["trigger_score"] +
        0.20 * scores["scene_fit_score"] +
        0.20 * scores["escalation_score"] +
        0.20 * scores["style_score"] +
        0.15 * scores["novelty_score"]
    )
```

### 評分重點

```text
trigger_score：
是否有合理的誤聽、諧音或語義錯位。

scene_fit_score：
是否充分利用輸入場景，而不是硬塞台灣。

escalation_score：
是否從小事件升級成群體、國際或物理異常。

style_score：
是否有莫名感動、外國人震撼、群體合唱、台灣精神收束。

novelty_score：
是否避免每次都長得一樣。
```

---

## 11. Safety Filter

本專案必須建立安全過濾層。

### 應避免內容

```text
1. 長篇直接複製歌曲歌詞
2. 嘲笑真實傷害或死亡事件
3. 針對特定真人的誹謗
4. 個資揭露
5. 仇恨或歧視
6. 暴力煽動
7. 非法行為教唆
```

### Safety Filter 虛擬碼

```python
def safety_filter(text: str):
    warnings = []

    if contains_long_lyrics(text):
        warnings.append("possible_copyright_issue")

    if mocks_real_victim(text):
        warnings.append("real_harm_mockery")

    if contains_private_info(text):
        warnings.append("private_information")

    if incites_violence(text):
        warnings.append("violence_incitement")

    return {
        "passed": len(warnings) == 0,
        "warnings": warnings
    }
```

---

## 12. API Token 設計

使用者可以自行輸入 API token 呼叫 LLM。

### 安全原則

```text
1. token 不應寫死在前端。
2. token 不應預設存入資料庫。
3. token 不應出現在 log。
4. token 應只在 session 或單次請求中暫存。
5. 錯誤訊息不可回傳完整 token。
6. 若提供記住 token 功能，必須加密儲存並允許刪除。
```

### 建議請求流程

```text
使用者在前端輸入 API token
  ↓
HTTPS 傳送到後端
  ↓
後端只在該次請求或 session 使用
  ↓
後端呼叫 LLM Provider
  ↓
回傳生成結果
```

不要讓前端直接呼叫 LLM API。  
那等於把 token 丟給瀏覽器環境，設計很醜。

---

## 13. FastAPI Endpoint 設計

### POST /api/scenario

用途：  
當使用者輸入不足時，產生候選情境。

Request:

```json
{
  "user_input": "我想要一個熱血、荒謬、科技風的複製文",
  "api_token": "user-provided-token",
  "provider": "openai",
  "model": "gpt-4.1-mini"
}
```

Response:

```json
{
  "mode": "ask_user_to_choose",
  "options": [
    {
      "id": "A",
      "title": "AI 實驗室爆肝型",
      "scene": "...",
      "characters": ["..."],
      "trigger_candidates": ["..."],
      "escalation_hint": "...",
      "tone": ["..."]
    }
  ]
}
```

---

### POST /api/generate

用途：  
生成完整複製文。

Request:

```json
{
  "user_input": "昨天在 Google Store 問 Pixel 用什麼處理器，店員說 Tensor",
  "api_token": "user-provided-token",
  "provider": "openai",
  "model": "gpt-4.1-mini"
}
```

Response:

```json
{
  "text": "...",
  "score": 0.91,
  "trigger_used": {
    "source": "Tensor",
    "misheard_as": "天色",
    "explanation": "...",
    "score": 0.92
  },
  "safety_passed": true,
  "warnings": []
}
```

---

### POST /api/generate-from-scenario

用途：  
使用者選擇候選情境後生成完整複製文。

Request:

```json
{
  "scenario_id": "A",
  "scenario": {
    "title": "AI 實驗室爆肝型",
    "scene": "...",
    "characters": ["研究生", "教授", "外籍交換生"],
    "trigger_candidates": ["Tensor error → 天色漸漸光"],
    "escalation_hint": "整棟資工系大樓開始合唱。",
    "tone": ["爆肝", "荒謬", "熱血"]
  },
  "user_revision": "加一點期末爆肝感",
  "api_token": "user-provided-token",
  "provider": "openai",
  "model": "gpt-4.1-mini"
}
```

---

## 14. 前端 UI 需求

### 頁面元素

```text
1. 使用者輸入框
2. API token 輸入框
3. LLM provider 選擇
4. model 選擇
5. 生成按鈕
6. 情境候選卡片
7. 使用者修改情境欄位
8. 生成結果展示區
9. 複製結果按鈕
10. 重新生成按鈕
```

### UI 流程

```text
使用者輸入需求
  ↓
按下分析 / 生成
  ↓
若資訊足夠：
    直接顯示生成結果
  ↓
若資訊不足：
    顯示 3~5 個情境選項
  ↓
使用者選擇或修改
  ↓
生成完整複製文
```

---

## 15. 部署架構

### 建議部署方式

```text
Client Browser
  ↓ HTTPS
Nginx
  ↓ Reverse Proxy
FastAPI Backend
  ↓
LLM Provider API
```

### 工作站部署範例

```text
university-workstation/
  /var/www/island-light-generator/frontend-dist
  /opt/island-light-generator/backend
  /etc/nginx/sites-available/island-light-generator
  /etc/systemd/system/island-light-generator.service
```

---

## 16. systemd 服務範例

```ini
[Unit]
Description=Island Light Generator FastAPI Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/island-light-generator/backend
Environment="PYTHONPATH=/opt/island-light-generator/backend"
ExecStart=/opt/island-light-generator/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 17. Nginx 設定範例

```nginx
server {
    listen 80;
    server_name your-domain.example.edu;

    location / {
        root /var/www/island-light-generator/frontend-dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

正式部署請使用 HTTPS。

---

## 18. .env.example

```env
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000

DATABASE_URL=sqlite:///./app.db

ALLOW_USER_API_TOKEN=true
STORE_USER_API_TOKEN=false

LOG_LEVEL=INFO
```

---

## 19. requirements.txt

```text
fastapi
uvicorn
pydantic
python-dotenv
httpx
sqlalchemy
pytest
```

如果之後要支援多 provider，可再加入各 provider SDK。  
初期建議先用 `httpx` 統一呼叫 API，避免被 SDK 綁死。

---

## 20. 開發順序

### Phase 1：純後端 MVP

```text
1. 建立 FastAPI 專案
2. 完成 InputProfile schema
3. 完成 Input Sufficiency Router
4. 完成 Scenario Expander
5. 完成 Trigger Miner
6. 完成 Draft Generator
7. 完成 Safety Filter
8. 用 CLI 或 Swagger 測試
```

### Phase 2：互動式 UI

```text
1. 建立前端輸入頁
2. 加入 API token 輸入
3. 顯示情境候選卡片
4. 支援使用者修改情境
5. 顯示最終生成結果
```

### Phase 3：部署

```text
1. 工作站建立 Python venv
2. 安裝 dependencies
3. 建立 systemd service
4. Nginx reverse proxy
5. 加入 HTTPS
6. 設定 rate limit
7. 確認 token 不寫入 log
```

---

## 21. 測試重點

```text
1. 模糊輸入是否會進 Scenario Expander
2. 具體輸入是否會直接生成
3. trigger 是否合理
4. 是否避免過度模板化
5. 是否不輸出長篇歌詞
6. 是否不記錄使用者 API token
7. 錯誤訊息是否不暴露 token
8. 前端重新整理後 token 是否不殘留
```

---

## 22. 核心設計結論

本專案不應設計成：

```text
輸入 → 套模板 → 輸出
```

而應設計成：

```text
輸入
  → 判斷資訊是否足夠
  → 補完情境
  → 找觸發梗
  → 建立敘事骨架
  → 多版本生成
  → 評分
  → 安全過濾
  → 輸出
```

簡單講：

```text
資訊足夠就分析。
資訊不足就先導演場景。
LLM 負責創意。
Rule 負責結構。
Scorer 負責品質。
Safety Filter 負責不要出事。
```
