# BugFix: DeepSeek reasoning_content + WebSearchApi

## 问题一：`reasoning_content` 丢失导致 400 错误

### 现象
```
openai.BadRequestError: Error code: 400 - {'error': {'message': 'The `reasoning_content` in the thinking mode must be passed back to the API.'}}
```

### 根因
DeepSeek v4 系列模型（包括 pro 和 flash）都会生成 `reasoning_content`（推理链）。API 要求多轮对话中，上一轮 assistant 消息里的 `reasoning_content` 必须原样传回。

LangChain 的 `langchain-openai` 在三个地方丢弃了它：

| 方向 | 函数 | 行号 | 问题 |
|------|------|------|------|
| 接收-非流式 | `_convert_dict_to_message` | base.py:198 | 只提取 `content`/`tool_calls`，忽略 `reasoning_content` |
| 接收-流式 | `_convert_delta_to_message_chunk` | base.py:428 | 同上；且 streaming 的 `reasoning_content` 在**不带 `role` 字段**的 delta 中 |
| 发送 | `_convert_message_to_dict` | base.py:346 | 不会从 `additional_kwargs` 中取出 `reasoning_content` 写回请求体 |

第二轮请求时 assistant 历史消息缺少 `reasoning_content`，API 校验失败返回 400。

### 修复
`src/agent/my_llm.py` 中 monkey-patch 了三个函数：

1. **接收端-非流式**：`_convert_dict_to_message` → 将 `reasoning_content` 存入 `AIMessage.additional_kwargs`
2. **接收端-流式**：`_convert_delta_to_message_chunk` → 同上，**关键是不限制 `role == "assistant"`**，因为 streaming 的 `reasoning_content` 所在的 delta 通常不带 role
3. **发送端**：`_convert_message_to_dict` → 从 `additional_kwargs` 中取出 `reasoning_content` 写回请求体

---

## 问题二：`'WebSearchApi' object is not callable`

### 现象
```
'WebSearchApi' object is not callable
搜索失败！:'WebSearchApi' object is not callable
```

### 根因
`zai` 库的 `ZhipuAiClient.web_search` 是一个 `WebSearchApi` 实例对象，不是可直接调用的方法。真正可调用的方法是 `client.web_search.web_search()`，多了一层命名空间。

### 修复
`src/agent/my_tools.py` 第 22 行：

```diff
- response = client.web_search(
+ response = client.web_search.web_search(
```
