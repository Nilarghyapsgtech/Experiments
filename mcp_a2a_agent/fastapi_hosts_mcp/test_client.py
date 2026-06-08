from fastmcp import Client
import asyncio
import httpx


MCP_URL="http://0.0.0.0:8000/mcp/"
def format_result(result:str):
    if hasattr(result,"text") and result.text is not None:
        return result.text
    if hasattr(result,"content") and result.content is not None:
        return "\n".join(getattr(item,"text",str(item)) for item in result.content)
    if hasattr(result,"data") and result.data is not None:
        return result.data
    
async def main():
    async with httpx.AsyncClient() as client:
        print(f"Health: {(await client.get("http://0.0.0.0:8000/health")).json()}")
    async with Client(MCP_URL) as client:
        tools=await client.list_tools()
        print(f"Tools:{[tool.name for tool in tools]}")
        print(f"Result:{format_result(await client.call_tool("reverse_text",{"text":"Welcome Back"}))}")
        print(f"Result:{format_result(await client.call_tool("word_length",{"text":"Welcome Back"}))}")
if __name__=="__main__":
    asyncio.run(main())

