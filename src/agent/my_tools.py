from langchain_core.tools import tool
from zai import ZhipuAiClient

from agent.env_utils import ZHIPU_API_KEY

client = ZhipuAiClient(
    api_key=ZHIPU_API_KEY
)

@tool('web_search', parse_docstring=True)
def web_search(query: str) -> str:
    """
    Search the web using the API.

    Args:
        query: Search query string.

    Returns:
        Search results as text.
    """
    try:
        response = client.web_search.web_search(
            search_engine='search_pro',
            search_query=query,
            count=3,
            search_recency_filter='noLimit'
        )
        if response.search_result:
            return '\n\n'.join([d.content for d in response.search_result])
        return '没有搜索到任何内容！'
    except Exception as e:
        print(e)
        return f'搜索失败！:{e}'