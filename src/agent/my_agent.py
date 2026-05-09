

from agent.my_tools import web_search

from deepagents import create_deep_agent
from agent.my_llm import llm 


agent = create_deep_agent( # create_agent
    model=llm,
    tools=[web_search],
    system_prompt="你是一个智能助手，能够使用工具进行网络搜索来回答用户的问题。请根据用户的提问，合理使用工具来获取信息，并给出准确的回答。"
)


