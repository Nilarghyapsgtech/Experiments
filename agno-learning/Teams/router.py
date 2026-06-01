from agno.agent import Agent
from agno.models.openai import OpenAIChat
from typing import Union,List
from agno.workflow import Step,Workflow,Router,StepInput
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools


load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

llm=OpenAIChat(id="gpt-4o-mini")

def route_by_topic(step_input: StepInput) -> Union[str, Step, List[Step]]:
    """Selector can return step name as string - Router resolves it."""
    topic = step_input.input.lower()

    if "tech" in topic or "ai" in topic or "software" in topic:
        return [hackernews_step]
    else:
        return [duckduckgo_step]

duckduckgo_search_agent = Agent(
    name="duckduckgo_search_agent",
    id="duckduckgo_search_123",
    model=llm,
    tools=[DuckDuckGoTools()],
    instructions="""
    You are a web search specialist.

    Responsibilities:
    - Search the web using DuckDuckGo.
    - Find relevant, recent, and authoritative sources.
    - Return concise summaries of findings.
    - Include source URLs for every claim.
    - Avoid speculation and unsupported conclusions.
    - Focus on gathering information, not analysis.

    Output Format:
    - Key Findings
    - Source Links
    - Relevant Quotes (if applicable)
    """
)

hackernews_agent = Agent(
    name="hackernews_agent",
    id="hackernews_agent_123",
    model=llm,
    tools=[HackerNewsTools()],
    instructions="""
    You are a Hacker News research specialist.

    Responsibilities:
    - Search Hacker News discussions relevant to the topic.
    - Identify community sentiment, debates, and expert opinions.
    - Highlight highly upvoted posts and comments.
    - Summarize technical insights and trends.
    - Provide links to original discussions.

    Output Format:
    - Discussion Summary
    - Key Community Insights
    - Notable Opinions
    - Hacker News Links
    """
)

research_agent = Agent(
    name="research_agent",
    id="research_agent_123",
    model=llm,
    instructions="""
    You are the lead research analyst.

    Responsibilities:
    - Coordinate information from other agents.
    - Compare and validate findings across sources.
    - Identify agreements, contradictions, and gaps.
    - Produce a comprehensive final report.
    - Cite all source references provided by sub-agents.

    Report Structure:
    1. Executive Summary
    2. Key Findings
    3. Supporting Evidence
    4. Contradictions and Limitations
    5. Conclusions
    6. References

    Prioritize accuracy, objectivity, and evidence-based reasoning.
    """
)

duckduckgo_step = Step(
    name="duckduckgo_step",
    agent=duckduckgo_search_agent,
    description="Search the web for relevant information, sources, and recent developments."
)

hackernews_step = Step(
    name="hackernews_step",
    agent=hackernews_agent,
    description="Gather community discussions, technical insights, and sentiment from Hacker News."
)

research_step = Step(
    name="research_step",
    agent=research_agent,
    description="Analyze and synthesize findings from all sources into a comprehensive research report."
)

router_step=Router(
    name="router-step",
    description="Routes search requests to the most relevant source based on the query topic.",
    choices=[duckduckgo_step,hackernews_step],
    selector=route_by_topic
)

search_workflow=Workflow(
    id="search_workflow_123",
    name="search_workflow",
    steps=[router_step,research_step],
    description="Performs topic-aware search and research by routing queries to the appropriate source."
)

search_workflow.print_response("Topic: Create a Topic about PM MODI",markdown=True,stream=True)
