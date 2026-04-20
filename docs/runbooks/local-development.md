# Local Development Runbook

這份 runbook 以 `_isolated_dev` 工作區為前提，所有命令都應在隔離區內執行，不要回頭修改原始根目錄。

## 前置需求

- Python 3.13
- Node.js 20+
- npm
- 可連線的 Supabase project 與 Gemini API key

## Backend 安裝

```powershell
cd D:\06_DailyWork\20260418_EvaluateSystem\_isolated_dev\backend
py -3 -m pip install -e .
```

如果已經有本機 virtualenv，也可以先啟用再執行相同安裝命令。

## Frontend 安裝

```powershell
cd D:\06_DailyWork\20260418_EvaluateSystem\_isolated_dev\frontend
npm install
```

## 環境變數

### `backend\.env`

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### `frontend\.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

## 本機啟動

### Backend

```powershell
cd D:\06_DailyWork\20260418_EvaluateSystem\_isolated_dev\backend
py -3 -m uvicorn app.main:app --reload --port 8000
```

### Frontend

目前 repo 的 `package.json` 只保留測試腳本；如果要在本機預覽 UI，可在 `frontend/` 內直接啟動 Vite。

```powershell
cd D:\06_DailyWork\20260418_EvaluateSystem\_isolated_dev\frontend
npx vite
```

## 測試

### Backend

```powershell
cd D:\06_DailyWork\20260418_EvaluateSystem\_isolated_dev\backend
py -3 -m pytest
```

### Frontend

```powershell
cd D:\06_DailyWork\20260418_EvaluateSystem\_isolated_dev\frontend
npm test
```

如果要先驗證單一頁面測試，可針對單檔執行 Vitest。

```powershell
npm test -- LoginPage.test.tsx
```

## Windows sandbox / Vitest EPERM 注意事項

- 在 Windows sandbox 或受限權限環境，Vitest 可能遇到 `EPERM`、`access denied` 或 cache lock 類錯誤
- 常見原因是 `node_modules/.vite`、temp 檔案或其他 Node process 正在占用檔案
- 建議先關掉多餘的 frontend dev server，再重跑測試
- 若仍失敗，先跑單一檔案測試，避免一次開太多 worker
- 這個 workspace 也曾出現 pytest cache 目錄的 access denied 訊息，因此測試輸出若提到 cache directory，不一定代表程式碼本身有錯

## Manual QA Checklist

### 登入與活動

- [ ] 老師使用 `teacher01 / secret123` 登入成功，回傳 `role=teacher`
- [ ] 老師建立活動成功，活動可綁定多個 assignment ids
- [ ] 學生使用 `student01 / secret123` 登入成功，回傳 `role=student`

### 提交流程

- [ ] 學生送出有效 XML 後，提交先進入 `queued` / 處理中狀態
- [ ] 學生送出無效 XML 時，API 立即回傳 `400 Invalid XML format`
- [ ] 提交後的處理流程會走 parser、rule engine、LLM 與 final decision

### 即時進度與燈號

- [ ] 老師 dashboard 在不手動 refresh 的情況下，能看到活動燈號變化
- [ ] WebSocket 連線建立後可維持活動 channel，`ping` 會回 `pong`
- [ ] 廣播事件能送到同一活動下的前端畫面

### 教師覆核

- [ ] 老師覆核可覆蓋學生原本看到的系統結果
- [ ] 覆核後的燈號與等第以教師結果為準
- [ ] 覆核原因會進入 audit / report 可追蹤的位置

### 課後報表

- [ ] 作業報表頁能顯示分布統計
- [ ] 報表能分辨紅 / 黃 / 綠 / 藍四燈號
- [ ] 報表結果與教師覆核後的結果一致

