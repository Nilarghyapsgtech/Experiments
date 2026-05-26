from agno.agent import Agent
from agno.models.openai import OpenAIChat
from knowledge_base import knowledge_base

session_id="knowledge_base_agent_1"
llm=OpenAIChat(id="gpt-4o-mini")

agent=Agent(
    model=llm,
    stream=True,
    markdown=True,
    instructions="""You are an AI assitant who asnwers questions, whenever asked about Transformers get Information from knowledge Base 
    Rest cases use your own Intelligence .Try not to hallucinate while giving an Answer
    """,
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.print_response("")
