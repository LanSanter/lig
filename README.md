# Island Light Generator

本專案依據 `README_island_light_generator.md`（規劃文件）實作完整可擴充架構，提供：

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

## 文件入口

- 架構說明：`docs/architecture.md`
- 部署流程：`docs/deployment.md`
