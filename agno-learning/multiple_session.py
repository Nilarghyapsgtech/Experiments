from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/nilasark/experiments/agno-learning/.env")

llm=OpenAIChat(id='gpt-4o-mini')

session_id_1="session_1"
session_id_2="session_2"
db=SqliteDb(db_file="Memory/session.db")

agent=Agent(
    model=llm,
    name="Agent-1",
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
    stream=True,
    db=db
)

agent.print_response("My name is Nilarghya",session_id=session_id_1)

agent.print_response("My Mom is Aparna",session_id=session_id_2)
agent.print_response("What is my name ?",session_id=session_id_1)
agent.print_response("What is my name ?",session_id=session_id_2)
agent.print_response("What is my Mom's name",session_id=session_id_2)