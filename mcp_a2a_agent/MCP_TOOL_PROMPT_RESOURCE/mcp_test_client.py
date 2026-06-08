from fastmcp import Client
import asyncio
from MCP_TOOL_PROMPT_RESOURCE.mcp import mcp

def format_result(result:str):
    if hasattr(result, "data") and result.data is not None:
        return result.data
    if hasattr(result, "text") and result.text is not None:
        return result.text
    if hasattr(result, "content"):
        return "\n".join(getattr(item, "text", str(item)) for item in result.content)
    if hasattr(result, "contents"):
        return [getattr(item, "text", str(item)) for item in result.contents]
    if hasattr(result, "messages"):
        return result.messages
    return str(result)

async def main():
    async with Client(mcp) as client:
        tools=await client.list_tools()
        resources=await client.list_resources()
        prompts=await client.list_prompts()
        print(tool.name for tool in tools)

        print(format_result(await client.call_tool("compare_temperatures",{"cityA":"mumbai","cityB":"london"})))
        print(format_result(await client.read_resource("weather://cities/mumbai")))
        print(format_result(await client.get_prompt("prompt_structure",{"city":"mumbai","audience":"traveller"})))

if __name__=="__main__":
    asyncio.run(main())

