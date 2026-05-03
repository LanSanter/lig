# Island Light Generator

本專案依據提供：

- FastAPI 後端（路由、服務層、資料模型）。
- Vue 3 + Tailwind 前端（狀態機式三階段互動）。
- 基礎測試與部署文件（Docker / Nginx / systemd）。

## 專案結構

```text
backend/
frontend/
docs/
```

## 快速啟動

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## One-shot Samples

- 範例檔案：`backend/data/oneshot_samples.json`
- 載入程式：`backend/services/sample_loader.py`
- 作用：scenario 與 generate 服務會讀取樣本進行動態輸出。

## 文件入口

- 架構說明：`docs/architecture.md`
- 部署流程：`docs/deployment.md`


## 後端 API Token 設定

- 前端不需要輸入 API Token。
- 前端也不需要傳送 provider，後端固定使用 OpenAI。
- 請在後端 `.env` 設定 `OPENAI_API_KEY`。
- 可選設定 `OPENAI_MODEL`，未設定預設 `gpt-4.1-mini`。
