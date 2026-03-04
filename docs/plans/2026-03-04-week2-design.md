# Week2 作业完成设计文档（2026-03-04）

## 1. 目标与范围

本次工作目标（满分导向）：

1. 完成 `week2/assignment.md` 的 TODO 1-5；
2. 保持后端/前端可运行、单元测试可重复执行；
3. 按要求填写 `week2/writeup.md`（个人信息先占位，最终回填）。

范围限定：

- 基于现有 `week2` 代码进行增量重构（不做整套 SQLAlchemy 迁移）。
- LLM 仅使用 Ollama（`ollama` Python SDK），结构化输出为 JSON 字符串数组。

## 2. 验收标准

### 2.1 功能验收

1. 现有启发式提取端点仍可用：`POST /action-items/extract`；
2. 新增 LLM 提取端点：`POST /action-items/extract-llm`；
   - LLM 可用时返回提取结果并写库；
   - LLM 不可用/解析失败等情况统一返回 `503`（不回退启发式）。
3. 新增 notes 列表端点：`GET /notes`；
4. 前端增加按钮并可交互：
   - `Extract`（启发式）
   - `Extract LLM`（LLM）
   - `List Notes`（列出所有 notes）

### 2.2 工程验收

- `uv run pytest week2/tests` 全绿；
- `uv run uvicorn week2.app.main:app --reload` 可启动并访问首页；
- 新增/修改的代码包含必要注释（标明 AI/工具生成的位置，便于评分）。

## 3. 交付物与对应 TODO

### TODO 1: LLM 提取函数

- 在 `week2/app/services/extract.py` 新增 `extract_action_items_llm()`：
  - 空输入直接返回 `[]`；
  - 默认模型：`OLLAMA_MODEL` 优先，否则 `llama3.1:8b`（本机现有）；
  - 使用 `ollama.chat(..., format=<JSON Schema>, options={"temperature": 0})` 强约束输出为 `list[str]`；
  - 做清洗/去重（保序、大小写不敏感）。

### TODO 2: 单元测试

- 在 `week2/tests/test_extract.py` 增加覆盖：
  - bullet/checkbox 风格输入
  - keyword 前缀输入（TODO/ACTION/等）
  - 空输入（断言不调用 LLM）
  - LLM 非法输出/异常路径（通过 monkeypatch/mock `ollama.chat` 隔离外部依赖）

### TODO 3: 后端重构（清晰度）

重点聚焦：

- API contract：新增 `week2/app/schemas.py`（Pydantic 请求/响应），路由不再使用裸 `Dict[str, Any]`；
- DB layer cleanup：`week2/app/db.py` 小幅整理（例如开启 `PRAGMA foreign_keys = ON`，收敛连接/初始化职责）；
- app lifecycle/config：将 `init_db()` 迁移到 FastAPI `startup`/`lifespan`，避免 import 副作用；
- error handling：服务层定义可识别异常（如 `LLMExtractionError`），路由层统一转换为 `HTTPException`（LLM 端点 `503`）。

### TODO 4: 新端点 + 前端按钮

- 新端点：
  - `POST /action-items/extract-llm`：与启发式端点返回结构一致
  - `GET /notes`：列出所有 notes（按 id 倒序）
- 前端（`week2/frontend/index.html`）：
  - 添加 `Extract LLM` / `List Notes` 两个按钮；
  - 显示 LLM `503` 的明确错误提示；
  - notes 列表渲染 `id/created_at/content`。

### TODO 5: week2 README

- 生成 `week2/README.md`（不是仓库根 README）：
  - 项目概览
  - 安装/运行（`uv sync --group dev`，`uv run uvicorn ...`）
  - API 端点与示例
  - 测试运行方式（`uv run pytest` / `uv run pytest week2/tests`）
  - LLM 端点对 `ollama serve` 与模型的依赖说明（不可用时返回 `503`）

## 4. API 设计（摘要）

- `POST /action-items/extract`
  - Request: `{ "text": str, "save_note": bool }`
  - Response: `{ "note_id": int | null, "items": [{ "id": int, "text": str }] }`
- `POST /action-items/extract-llm`
  - Request/Response 同上
  - Failure: `503`（detail 统一）
- `GET /notes`
  - Response: `[{ "id": int, "content": str, "created_at": str }]`

## 5. 风险与回退

- 风险：本机 `llama3.1:8b` 资源占用偏高导致响应慢。
  - 缓解：将模型通过 `OLLAMA_MODEL` 可配置；测试用 mock 避免依赖模型可用性。
- 风险：LLM 输出格式漂移。
  - 缓解：使用 JSON Schema structured outputs + 严格解析/校验 + 失败即 `503`。

## 6. Writeup 要求

- `week2/writeup.md` 中每个 Exercise 记录：
  - 使用的 prompt（本次对话/实现时的关键指令）
  - 修改的文件与关键函数/端点位置（尽量附行号）
- 个人信息（Name/SUNet ID/Citations/耗时）先保持占位符，最终回填。

