from fastmcp import Client
import asyncio
from mcp_02 import mcp
def format_result(result):
    if hasattr(result,"text") and result.text is not None:
        return result.text
    if hasattr(result,"data") and result.data is not None:
        return result.data
    if hasattr(result,"content") and result.content is not None:
        return "\n".join(getattr(item,"text",str(item)) for item in result.content)

async def main():
    async with Client(mcp) as client:
        tools=await client.list_tools()
        print([tool.name for tool in tools])
        result=await client.call_tool("weather_forecast",{"city":"london","days":2})
        print(format_result(result))
if __name__=="__main__":
    asyncio.run(main())

        