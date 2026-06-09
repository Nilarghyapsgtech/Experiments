from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("/Users/nilasark/experiments/mcp_a2a_agent/env")
llm=OpenAIChat(id='gpt-4o-mini')

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(f"OPENAI_API_KEY is not set in the Environment")
    mcp_tools=MCPTools(
        transport='streamable-http',
        url="http://127.0.0.1:8000/mcp"
    )
    await mcp_tools.connect()
    try:
        agent=Agent(
            model=llm,
            name="mcp_agent",
            tools=[mcp_tools],
            instructions="""You are a calculator agent. For arithmetic, always call the MCP tool.""",
            markdown=True,
            stream=True,
        )
        await agent.aprint_response("Use the MCP tool to calculate 19 + 23. Return the tool name and final number.")
    finally:
        await mcp_tools.close()

if __name__=="__main__":
    asyncio.run(main())

