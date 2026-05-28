from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
from agno.run import RunContext

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

llm=OpenAIChat(id='gpt-4o-mini')
session_context={"grocery_list":[],"todo_list":[],"study_list":[]}

db=SqliteDb(db_file="/Users/nilasark/experiments/agno-learning/Memory/teams_context.db",session_table="team_context")

def add_item(run_context:RunContext,item:str,list_name:str):
    """Add Specified item to the Specified list_name"""
    list_name=list_name.lower()
    item=item.lower()
    if run_context.session_state[list_name].__contains__(item):
        return f"{item} already exists in the List"
    run_context.session_state[list_name].append(item)
    return f"{item} added to List"

def remove_item(run_context:RunContext,item:str,list_name:str):
    """Remove Specified item to the Specified list_name"""
    item=item.lower()
    list_name=list_name.lower()
    if run_context.session_state[list_name].__contains__(item):
        run_context.session_state[list_name].remove(item)
        return f"{item} removed from the list"
    return f"{item} doesnot Exist in the List"

def list_items(run_context:RunContext,list_name:str):
    """Shows Specified list_name"""
    list_name=list_name.lower()
    return "\n".join( run_context.session_state[list_name])
def clear_list(run_context:RunContext,list_name:str):
    """Clears specified list_name"""
    list_name=list_name.lower()
    run_context.session_state[list_name].clear()
    return f"The List is Empty now"     


GroceryAgent=Agent(
    id="grocery_agent_123",
    name="grocery_agent",
    role="You are a Grocery agent who manages list of items in a grocery_list",
    instructions="""
                    - You are an Expert in managing grocery_list
                    - You can add items to the grocery_list through add_item tool
                    - You can remove items to the grocery_list through remove_item tool
                    - You can clear the grocery_list through clear_list tool
                    - You can show the Entire List through list_items tool
                 """,
    model=llm,
    tools=[add_item,remove_item,list_items,clear_list]
)

StudyAgent=Agent(
    id="study_agent_123",
    name="study_agent",
    role="You are a Study agent who manages list of items in a study_list",
    instructions="""
                    - You are an Expert in managing study_list 
                    - You can add items to the study_list through add_item tool
                    - You can remove items to the study_list through remove_item tool
                    - You can clear the study_list through clear_list tool
                    - You can show the Entire study_list through list_items tool
                 """,
    model=llm,
    tools=[add_item,remove_item,list_items,clear_list]
)

TodoAgent=Agent(
    id="todo_agent_123",
    name="todo_agent",
    role="You are a Todo agent who manages list of items in a todo_list",
    instructions="""
                    - You are an Expert in managing todo_list
                    - You can add items to the todo_list through add_item tool
                    - You can remove items to the todo_list through remove_item tool
                    - You can clear the todo_list through clear_list tool
                    - You can show the Entire todo_list through list_items tool
                 """,
    model=llm,
    tools=[add_item,remove_item,list_items,clear_list]
)

ManagerAgent=Team(
    members=[GroceryAgent,StudyAgent,TodoAgent],
    id="manager_agent_id",
    name="manager_agent",
    role="You are a manager agent who divides the Total task among the correct member agent to complete the Task ",
   instructions="""
- You are a routing and coordination agent.
- Your job is to detect list-management requests and delegate them to exactly one specialist agent.
- Treat any sentence that expresses a personal plan, errand, goal, reminder, or action item as a todo item unless it clearly belongs to grocery_list or study_list.
- Map the request to the correct list using meaning, not only exact keywords.
- Route these kinds of requests to TodoAgent:
  - "I want to go to gym"
  - "Remind me to work out"
  - "Need to call mom"
  - "Buy groceries tomorrow"
- Route grocery-related requests to GroceryAgent.
- Route study-related requests to StudyAgent.
- If the request mentions multiple lists, split it into separate sub-tasks and route each part to the correct agent.
- Do not answer directly when the user is asking to add, remove, show, or clear a list item.
- Do not mix list contents across categories.
- If the user asks to show a list, return only that list.
- Keep responses short, direct, and action-oriented.
""",
    model=llm,
    stream=True,
    markdown=True,
    session_state=session_context,
    add_session_state_to_context=True,
    db=db,
)

ManagerAgent.cli_app(stream=True,markdown=True)