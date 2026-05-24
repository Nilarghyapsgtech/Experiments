from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run import RunContext
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

llm=OpenAIChat(id="gpt-4o-mini")
db=SqliteDb(db_file="/Users/nilasark/experiments/agno-learning/Memory/web_search")
web_search_tool=DuckDuckGoTools(enable_search=True,fixed_max_results=5)
agent=Agent(
    name="web-search-agent",
    model=llm,
    markdown=True,
    stream=True,
    add_session_state_to_context=True,
    tools=[web_search_tool],
    instructions="""
        You are a websearch agent who specializes in providing in specializing information to Question.
        {Question}:{Answer}
    """
)

agent.print_response("Give all Important news of India")

