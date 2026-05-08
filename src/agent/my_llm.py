import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_openai import ChatOpenAI
from agent.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

llm = ChatOpenAI(
    model="deepseek-v4-pro",
    temperature=1.1,
    openai_api_key=DEEPSEEK_API_KEY,
    openai_api_base=DEEPSEEK_BASE_URL,
)

resp = llm.invoke('测试链接，回复链接成功或不成功')
print(resp)