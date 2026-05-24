from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
from agno.run import RunContext

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

llm=OpenAIChat(id='gpt-4o-mini')

db=SqliteDb(db_file="Memory/session_context.db")
session_id="session_2"
session_context={"shopping_list":[]}


# def edit_shopping_list(run_context: Run_Context, item):
#     run_context.session_state["shopping_list"].append(item)
    

def edit_shopping_list(run_context:RunContext,item):
    item=item.lower()
    if run_context.session_state["shopping_list"].__contains__(item):
        return f"{item.upper()} is already in the Shopping List"
    run_context.session_state["shopping_list"].append(item)
    return f"The new shopping_list is {run_context.session_state['shopping_list']}"

def remove_item_from_shopping_list(run_context:RunContext,item):
    item=item.lower()
    if not run_context.session_state["shopping_list"].__contains__(item):
        return f"{item.upper()} is not in the Shopping List"
    run_context.session_state["shopping_list"].remove(item)
    return f"The new shopping_list is {run_context.session_state['shopping_list']}"

agent=Agent(
    name="session_context_agent",
    id="agno_session_context",
    model=llm,
    session_id=session_id,
    markdown=True,
    stream=True,
    session_state=session_context,
    instructions="""You maintain a shopping list.

Current shopping list:
{shopping_list}

Rules:
- When user asks to add an item, ALWAYS use the add_to_shopping_list tool.
- When User asks to he bought an item or to remove an item or similar statement use the remove_item_from_shopping_list tool.
- When user asks what is in the shopping list, answer from session state.""",
    tools=[edit_shopping_list,remove_item_from_shopping_list],
    add_session_state_to_context=True,
    db=db
)

agent.print_response("Add Beer to my shopping list")
agent.print_response("add Wine to my shopping List")

agent.print_response("No need for  Beer in my shopping List")

agent.print_response("What all are in My shopping List")



