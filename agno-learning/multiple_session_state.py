from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.run import RunContext
from dotenv import load_dotenv

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

sessiion_id_grocery="Grocery_list"
sessiion_id_electronics="Electronics"

db=SqliteDb("Memory/session_context.db")
llm=OpenAIChat(id="gpt-4o-mini")

session_context={"shopping_list":[]}

def add_to_shopping_list(run_context:RunContext,item:str):
    if run_context.session_state["shopping_list"].__contains__(item):
        return f"{item.upper()} already exists in the List"
    run_context.session_state["shopping_list"].append(item)
    return f"The current shopping list is {run_context.session_state["shopping_list"]}"

def remove_item_from_shopping_list(run_context:RunContext,item:str):
    if run_context.session_state["shopping_list"].__contains__(item):
        run_context.session_state["shopping_list"].remove(item)
        return f"{item} is removed from the List"
    return f"{item} doesn't exist in the list"


agent=Agent(
    name="shopping-agent",
    db=db,
    model=llm,
    markdown=True,
    stream=True,
    add_session_state_to_context=True,
    tools=[add_to_shopping_list],
    session_state=session_context,
    instructions="""
    You are an Agent who specalizes in making shopping list for grocery and Electronics.
    The current shopping List is {shopping_list}
    Rules:
    - When user asks  to add an item or buy an item, ALWAYS use the add_to_shopping_list tool.
    - When User asks to he bought an item or to remove an item or similar statement use the remove_item_from_shopping_list tool.
    - When user asks what is in the shopping list, answer from session state.""",

)

agent.print_response("Buy onions",session_id=sessiion_id_grocery)
agent.print_response("Buy Calculator",session_id=sessiion_id_electronics)
agent.print_response("Show my shopping List",session_id=sessiion_id_grocery)
# agent.print_response("Show my shopping List",session_id=sessiion_id_electronics)
