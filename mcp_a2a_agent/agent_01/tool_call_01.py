from fastmcp import Client
from mcp_01 import mcp
import asyncio




def rendered_result(result):
    if hasattr(result,"data") and result.data is not None:
        return result.data
    if hasattr(result,"text") and result.text is not None:
        return result.text
    if hasattr(result,"content") and result.content is not None:
        return "\n".join(getattr(item,"text",str(item)) for item in result.content)
    return result


async def main():
    async with Client(mcp) as client:
        tools=client.list_tools()
        print("tools:" ,[tool.name for tool in tools])
        result=client.call_tool("add",{"a":10,"b":40})
        print(f"sum(10,40) is {rendered_result(result)}")

if __name__=="__main__":
    asyncio.run(main())