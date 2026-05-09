# ScratchClaw

[English](README.md) | [中文](README_CN.md)

> Build an AI coding agent from scratch — a hands-on reimplementation of Claude Code/OpenClaw, step by step.

## Overview

ScratchClaw is an educational project that rebuilds an AI-powered coding agent from the ground up. Instead of using a black-box CLI, this project dissects every component — LLM interaction, tool execution, agent loop, and sandbox — so you can understand how modern AI coding agents work under the hood.

## Getting Started

```bash
git clone https://github.com/sinha404/ScratchClaw.git
cd ScratchClaw
pip install -e .
```

Copy `.env.example` to `.env` (or create one) and fill in your API keys:

```env
DEEPSEEK_API_KEY=your_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Project Structure

```
src/agent/          # Core agent logic
  my_llm.py         # LLM configuration
  my_tools.py       # Tool definitions
  env_utils.py      # Environment variable loading
  graph.py          # LangGraph workflow definition
```

## License

MIT
