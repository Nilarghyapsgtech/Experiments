from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv
import asyncio

load_dotenv("/Users/nilasark/experiments/mcp_a2a_agent/.env")
llm=OpenAIChat(id='gpt-4o-mini')

mcp_tools=MCPTools(
    transport='streamable-http',url="http://127.0.0.1:8000/mcp"
)


def discover_tools(mcp_tools:MCPTools):
    function=getattr(mcp_tools,"functions",None)
    if isinstance(function,dict):
        return sorted(function.keys())
    tools=getattr(mcp_tools,"tools",None)
    if isinstance(tools,list):
         return sorted(str(tool) for tool in tools)
    return ["<Tools are handled Internally by Agno>"]



async def main():
    mcp_tools=MCPTools(
    transport='streamable-http',url="http://127.0.0.1:8000/mcp"
)   
    await mcp_tools.connect()
    try:
        print("Discovered MCP tools:", discover_tools(mcp_tools))
        agent=Agent(
            name="mcp_agent",
            model=llm,
            instructions="""
                        You are a calculator agent. For arithmetic, always call the MCP tool.
                         """,
            tools=[mcp_tools],
            markdown=True,
            stream=True
        )

        await agent.aprint_response("what is the value of 8 to the power 3")
    finally:
        await mcp_tools.close()

if __name__=="__main__":
    asyncio.run(main())
