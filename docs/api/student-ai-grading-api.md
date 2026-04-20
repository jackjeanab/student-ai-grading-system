# Student AI Grading API

這份文件只描述目前 backend 已經實作的端點與行為，不補不存在的 CRUD 或完整權限系統。

## 共通約定

- Base URL: 依部署環境而定
- 認證目前是字串 token 比對，不是完整 JWT 驗證
- `teacher` 相關端點使用 `Authorization: Bearer dev-token`
- `student` 提交端點使用 `Authorization: Bearer student-token`
- 除了明確標示的例外，錯誤格式沿用 FastAPI 預設的 `{"detail": "..."}` 或 validation error

## 端點總覽

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/health` | 健康檢查 |
| POST | `/api/auth/login` | 登入並回傳角色與 access token |
| POST | `/api/activities` | 老師建立課堂活動 |
| POST | `/api/submissions` | 學生提交 XML 作業 |
| POST | `/api/teacher/submissions/{submission_id}/override` | 老師覆核覆蓋結果 |
| GET | `/api/reports/assignments/{assignment_id}` | 作業報表 |
| WS | `/ws/activities/{activity_id}` | 活動即時通道 |

## 健康檢查

### `GET /health`

回傳服務是否可用。

**Response 200**

```json
{"status":"ok"}
```

## 登入

### `POST /api/auth/login`

**Request**

```json
{
  "account": "teacher01",
  "password": "secret123"
}
```

**Response 200**

```json
{
  "access_token": "dev-token",
  "role": "teacher"
}
```

**失敗**

- `401 Invalid credentials`

目前實作只有兩組測試帳號：

- `teacher01 / secret123`
- `student01 / secret123`

## 活動

### `POST /api/activities`

建立課堂活動。

**Header**

```http
Authorization: Bearer dev-token
```

**Request**

```json
{
  "title": "Chapter 2 Practice",
  "assignment_ids": [101, 102],
  "status": "draft"
}
```

**Response 201**

```json
{
  "id": 1,
  "title": "Chapter 2 Practice",
  "assignment_ids": [101, 102],
  "status": "draft"
}
```

**失敗**

- `401 Unauthorized`

## 提交

### `POST /api/submissions`

學生提交 XML 作業後，backend 會先驗證 XML，再呼叫 parser、rule engine、LLM 與 final decision 流程。現階段回應是 queued，沒有在這個 endpoint 直接回傳完整評分結果。

**Header**

```http
Authorization: Bearer student-token
```

**Request**

```json
{
  "assignment_id": 101,
  "activity_id": 1,
  "xml_content": "<xml>...</xml>"
}
```

**Response 202**

```json
{"status":"queued"}
```

**失敗**

- `400 Invalid XML format`
- `401 Unauthorized`

## 老師覆核

### `POST /api/teacher/submissions/{submission_id}/override`

老師可用人工覆核覆蓋系統結果。這個 endpoint 直接回傳覆核後的結果，不會再包一層 submission model。

**Header**

```http
Authorization: Bearer dev-token
```

**Request**

```json
{
  "grade": "優",
  "light": "green",
  "reason": "Teacher review"
}
```

**可用 grade**

- `優`
- `良`
- `可`
- `待加強`

**可用 light**

- `green`
- `blue`
- `yellow`
- `red`

**Response 200**

```json
{
  "submission_id": 1,
  "grade": "優",
  "light": "green",
  "reason": "Teacher review",
  "teacher_revised": true
}
```

**失敗**

- `401 Unauthorized`
- `422` schema validation error

## 報表

### `GET /api/reports/assignments/{assignment_id}`

回傳單一作業的報表資料。目前實作先回傳空 rows，作為後續統計與匯整的接口。

**Response 200**

```json
{
  "assignment_id": 101,
  "rows": []
}
```

## 作業路由

### `/api/assignments`

目前已建立 router，但尚未掛任何 handler。文件上只保留這個 base path，避免假設已存在未實作的 CRUD 端點。

## 即時通道

### `WS /ws/activities/{activity_id}`

這條通道是活動層級的 WebSocket channel。現階段已實作的行為如下：

- 連線建立後會接受 `ping`
- 收到 `ping` 會回 `pong`
- 其他文字訊息會回 `unsupported_message`
- 應用程式若呼叫 hub broadcast，會透過 `send_json(payload)` 送出 JSON 物件

**文字訊息範例**

```text
ping
```

**回應**

```text
pong
```

目前沒有固定的事件 envelope 規格，因此前端在解讀廣播 payload 時，應依實際送出的 JSON 結構處理。

