from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")


llm=OpenAIChat(id="gpt-4o-mini")

price_agent=Agent(
    name="Price Agent",
    id="Price_Agent",
    model=llm,
    role="You are a an Agent specialized in getting Details about the Price an Item",
    instructions="""
        You get the Details about the Price of an Item in Indian Curreny and Display it Proper Format
        """,
    tools=[DuckDuckGoTools()]
    )

quality_agent=Agent(
    name="Quality Agent",
    id="Quality_Agent",
    model=llm,
    role="You are a an Agent specialized in getting Details about the Quality an Item",
    instructions="""
        You get the Details about the Quality of an Item and Display it Proper Format
        """,
    tools=[DuckDuckGoTools()]
)

information_agent=Team(
    members=[price_agent,quality_agent],
    name="Information Agent",
    id="Information_Agent",
    model=llm,
    role="You are a Leader Agent who Invokes your member agents to complete the Task",
    instructions="""
    You are a Leader Agent who Invokes your member agents to complete the Task,
    You consolidate the Output of bot the member agents and give a summarized Output
    """,
    markdown=True,
    stream=True

)

information_agent.cli_app(markdown=True,stream=True)
