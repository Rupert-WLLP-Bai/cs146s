# Week1 作业完成设计文档（2026-03-04）

## 1. 目标与范围

本次工作目标：

1. 在新分支完成 `week1` 的全部提示工程 TODO；
2. 按“严格可运行”标准在本机真实运行验证（`ollama` + 指定模型）；
3. 通过 PR 合并到 `master`。

范围限定：

- 仅修改以下文件中的 TODO 位置：
  - `week1/k_shot_prompting.py`
  - `week1/chain_of_thought.py`
  - `week1/tool_calling.py`
  - `week1/self_consistency_prompting.py`
  - `week1/rag.py`
  - `week1/reflexion.py`
- 不改题目框架逻辑、模型名称、测试主流程（除非为修复明显运行故障且有最小改动）。

## 2. 验收标准

### 2.1 功能验收

每个脚本单独运行，输出包含 `SUCCESS`：

1. `week1/k_shot_prompting.py`
2. `week1/chain_of_thought.py`
3. `week1/tool_calling.py`
4. `week1/self_consistency_prompting.py`
5. `week1/rag.py`
6. `week1/reflexion.py`

### 2.2 工程验收

- 新分支开发；
- 提交包含 TODO 完成与必要文档；
- PR 指向 `master`；
- PR 合并后 `master` 同步最新提交。

## 3. 实施策略

### 3.1 环境准备

1. 安装 `ollama`；
2. 启动服务（`ollama serve`）；
3. 拉取模型：
   - `mistral-nemo:12b`
   - `llama3.1:8b`
4. 确认 `ollama list` 可见模型。

### 3.2 提示词设计原则

- 高约束输出格式：减少模型自由度；
- 明确禁止额外文本（尤其是 JSON/代码块边界外内容）；
- 任务导向：只给完成当前脚本需要的信息；
- 对不稳定任务使用“最终答案行”约束与格式回退策略。

### 3.3 各脚本设计要点

#### A. `k_shot_prompting.py`

- 使用 few-shot 示例展示“输入词 -> 仅输出反转词”；
- 明确“只能输出一个词”。

#### B. `chain_of_thought.py`

- 允许推理；
- 强制最后一行严格为 `Answer: <number>`。

#### C. `tool_calling.py`

- 强制输出严格 JSON 对象（无 markdown）；
- `tool` 固定为 `output_every_func_return_type`；
- `args` 包含 `file_path` 指向当前脚本（可用 `week1/tool_calling.py`）。

#### D. `self_consistency_prompting.py`

- 强调逐步计算但仅把最终值写到 `Answer: <number>`；
- 减少格式漂移，配合多数投票提升稳定性。

#### E. `rag.py`

- `YOUR_CONTEXT_PROVIDER` 返回 API 文档上下文（`corpus[0]`）；
- 系统提示限制“只依据 context 生成函数代码块”；
- 确保包含 required snippets。

#### F. `reflexion.py`

- 初始反思提示要求“根据失败用例修复，仅输出代码块”；
- `your_build_reflexion_context` 拼接：
  - 上一版代码；
  - 失败列表；
  - 保持签名与输出要求。

## 4. 风险与回退

### 4.1 主要风险

- `mistral-nemo:12b` 下载耗时或显存不足；
- 某些脚本存在非确定性输出；
- tool calling 任务易出现非 JSON 文本污染。

### 4.2 处理策略

- 多次运行验证稳定性；
- 先收紧格式约束，再微调 prompt；
- 如出现模型资源问题，记录阻塞并给出替代验证路径。

## 5. 执行记录要求

- 记录每个脚本的执行命令与关键结果；
- 记录每次 prompt 修改的意图；
- 在 `week1` 留存同日执行记录文件；
- 将完整记录同步到博客文档路径。

## 6. Git / PR 计划

1. 创建分支：`feat/week1-complete`；
2. 完成修改 + 本地验证；
3. 提交信息：`Complete week1 prompting assignment with verified runs`；
4. 推送并创建 PR；
5. 合并 PR 到 `master`。

