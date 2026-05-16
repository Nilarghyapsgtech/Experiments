# --------------------- Initialization of Repo --------------------------

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.in_memory import InMemoryDb
from agno.db.sqlite import SqliteDb
from agno.db.json import JsonDb

from dotenv import load_dotenv

load_dotenv(dotenv_path='/Users/nilasark/experiments/agno-learning/.env')

llm=OpenAIChat(id='gpt-4o-mini')

session_id="session_1"

in_memory_db=InMemoryDb()
json_db=JsonDb(db_path="Memory",session_table="session")
sqlite_db=SqliteDb(db_file="Memory/session.db")

#-----------------------Agent Initialization------------------------------
agent=Agent(
    model=llm,
    name='my-agno-agent',
    markdown=True,
    db=sqlite_db,
    session_id=session_id,
    add_history_to_context=True,
    num_history_runs=3,
    stream=True
)


# agent.print_response("My name is Nilarghya")
agent.print_response("My name is ram")
agent.print_response("Can you tell my name ?")

messages=agent.get_chat_history(session_id)


for message in messages:
    role,content=message.role,message.content
    print(f"The message of {role} is {content}")
