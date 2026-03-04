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

- [ ] `ollama -v`
- [ ] `ollama list`
- [ ] `ollama serve` 正常运行

### 模型准备

- [ ] `mistral-nemo:12b`
- [ ] `llama3.1:8b`

### 代码与验证

- [ ] `week1/k_shot_prompting.py`
- [ ] `week1/chain_of_thought.py`
- [ ] `week1/tool_calling.py`
- [ ] `week1/self_consistency_prompting.py`
- [ ] `week1/rag.py`
- [ ] `week1/reflexion.py`

### Git / PR

- [ ] 提交完成
- [ ] 推送分支
- [ ] 创建 PR
- [ ] 合并 PR

## 结果摘要

（待实现完成后补充）

