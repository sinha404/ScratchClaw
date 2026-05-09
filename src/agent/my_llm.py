import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_openai import ChatOpenAI
from langchain_openai.chat_models import base as openai_base
from agent.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- Monkey-patch: preserve reasoning_content for DeepSeek thinking mode ---

# 1) 接收端 - 非 streaming 路径
_original_convert_dict_to_message = openai_base._convert_dict_to_message


def _patched_convert_dict_to_message(_dict):
    message = _original_convert_dict_to_message(_dict)
    if _dict.get("role") == "assistant" and "reasoning_content" in _dict:
        message.additional_kwargs["reasoning_content"] = _dict["reasoning_content"]
        # print(f"[PATCH] 接收(非流式) 保存 reasoning_content，长度: {len(_dict['reasoning_content'])}")
    return message


openai_base._convert_dict_to_message = _patched_convert_dict_to_message

# 2) 接收端 - streaming 路径 (agent 实际走的路径)
_original_convert_delta_to_message_chunk = openai_base._convert_delta_to_message_chunk


def _patched_convert_delta_to_message_chunk(_dict, default_class):
    chunk = _original_convert_delta_to_message_chunk(_dict, default_class)
    if "reasoning_content" in _dict:
        rc = _dict["reasoning_content"]
        if rc:
            chunk.additional_kwargs["reasoning_content"] = rc
            # print(f"[PATCH] 接收(流式) 保存 reasoning_content，长度: {len(rc)}")
    return chunk


openai_base._convert_delta_to_message_chunk = _patched_convert_delta_to_message_chunk

# 3) 发送端
_original_convert_message_to_dict = openai_base._convert_message_to_dict


def _patched_convert_message_to_dict(message, api="chat/completions"):
    result = _original_convert_message_to_dict(message, api=api)
    if result.get("role") == "assistant":
        reasoning = message.additional_kwargs.get("reasoning_content")
        if reasoning:
            result["reasoning_content"] = reasoning
            # print(f"[PATCH] 发送端回传 reasoning_content，长度: {len(reasoning)}")
    return result


openai_base._convert_message_to_dict = _patched_convert_message_to_dict

print("[PATCH] reasoning_content 补丁已激活 (含 streaming)")

# ------------------------------------------------------------------------

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=1.1,
    openai_api_key=DEEPSEEK_API_KEY,
    openai_api_base=DEEPSEEK_BASE_URL,
)


