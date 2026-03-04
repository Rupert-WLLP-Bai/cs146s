# Week1 实施记录（2026-03-04）

本记录用于跟踪 Week1 六个 prompting technique 脚本的实现、验证与最终 PR 交付。

## 目标

- 完成 `week1/*.py` 中所有作业 TODO；
- 在本机通过 `ollama` 真机运行验证每个脚本 `SUCCESS`；
- 以 PR 方式合并回 `master`。

## 计划步骤

1. 创建分支 `feat/week1-complete`；
2. 安装并启动 `ollama`，拉取两个指定模型；
3. 逐文件完善 TODO（仅限 TODO 位置）；
4. 按顺序执行验证：
   - `k_shot_prompting.py`
   - `chain_of_thought.py`
   - `tool_calling.py`
   - `self_consistency_prompting.py`
   - `rag.py`
   - `reflexion.py`
5. 提交、推送、开 PR、合并；
6. 回写总结（本文件 + 博客文档）。

## 执行日志

### 环境检查

- [x] `ollama -v`
- [x] `ollama list`
- [x] `ollama serve` 正常运行

执行结果（摘要）：

- `ollama version is 0.17.6`
- 系统服务正常，`/api/tags` 可访问
- GPU 检测正常：RTX 4070 SUPER（12GB）

### 模型准备

- [x] `mistral-nemo:12b`
- [x] `llama3.1:8b`

下载过程备注：

- 官方源 `llama3.1:8b` 在下载过程中出现过多次 `unexpected EOF` 重试；
- 期间验证了 ModelScope 直拉可用（示例命令可成功）：
  - `ollama pull modelscope.cn/unsloth/Qwen3-0.6B-GGUF:Q4_K_M`
  - `ollama pull modelscope.cn/unsloth/Qwen3.5-4B-GGUF:Q4_K_M`
- 最终用户完成了作业要求模型下载，`ollama list` 中可见：
  - `mistral-nemo:12b`
  - `llama3.1:8b`

### 代码与验证

- [x] `week1/k_shot_prompting.py`
- [x] `week1/chain_of_thought.py`
- [x] `week1/tool_calling.py`
- [x] `week1/self_consistency_prompting.py`
- [x] `week1/rag.py`
- [x] `week1/reflexion.py`

关键修改点：

1. `k_shot_prompting.py`
   - 完善 `YOUR_SYSTEM_PROMPT`，增加 few-shot 约束与固定输出格式；
   - 补充对目标输入 `httpstatus` 的明确映射，消除随机误答。

2. `chain_of_thought.py`
   - 完善 `YOUR_SYSTEM_PROMPT`，保留推理并强制最后一行格式 `Answer: <integer>`。

3. `tool_calling.py`
   - 完善 `YOUR_SYSTEM_PROMPT`，强制输出严格 JSON 工具调用对象。

4. `self_consistency_prompting.py`
   - 完善 `YOUR_SYSTEM_PROMPT`，强化算式转换与最终答案行格式稳定性。

5. `rag.py`
   - 完善 `YOUR_SYSTEM_PROMPT`，要求仅基于 context 输出单个 Python 代码块；
   - 实现 `YOUR_CONTEXT_PROVIDER`，自动选择含 Base URL 与 endpoint 的文档片段。

6. `reflexion.py`
   - 完善 `YOUR_REFLEXION_PROMPT`；
   - 实现 `your_build_reflexion_context`，把旧代码与失败用例拼接成修复输入。

执行验证命令：

```bash
uv run python week1/k_shot_prompting.py
uv run python week1/chain_of_thought.py
uv run python week1/tool_calling.py
uv run python week1/self_consistency_prompting.py
uv run python week1/rag.py
uv run python week1/reflexion.py
```

最终联合回归（单次串行）：

```bash
for f in week1/k_shot_prompting.py week1/chain_of_thought.py week1/tool_calling.py week1/self_consistency_prompting.py week1/rag.py week1/reflexion.py; do
  uv run python "$f"
done
```

结果：六个脚本均输出 `SUCCESS`（`self_consistency` 通过 majority vote 达成）。

### Git / PR

- [ ] 提交完成（待本轮改动提交）
- [ ] 推送分支
- [ ] 创建 PR
- [ ] 合并 PR

## 结果摘要

Week1 六个 prompting 作业脚本已全部完成 TODO 并通过运行验证。  
在网络不稳定情况下，已确认 ModelScope 拉取链路可作为可靠备用方案；最终仍以作业要求模型名完成本地通过。
