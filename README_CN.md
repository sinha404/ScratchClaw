# ScratchClaw

[English](README.md) | [中文](README_CN.md)

> 从零手撕 AI 编程智能体 —— 一步步复刻 Claude Code/OpenClaw 的实现。

## 概述

ScratchClaw 是一个教学项目，从零构建 AI 编程智能体。不依赖黑盒 CLI，逐层拆解 LLM 交互、工具执行、Agent 循环、沙箱等核心组件，让你彻底理解现代 AI 编程智能体的工作原理。

## 快速开始

```bash
git clone https://github.com/sinha404/ScratchClaw.git
cd ScratchClaw
pip install -e .
```

复制 `.env.example` 为 `.env`（或手动创建），填入你的 API Key：

```env
DEEPSEEK_API_KEY=your_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## 项目结构

```
src/agent/          # 核心 Agent 逻辑
  my_llm.py         # LLM 配置
  my_tools.py       # 工具定义
  env_utils.py      # 环境变量加载
  graph.py          # 工作流定义
```

## 许可证

MIT
