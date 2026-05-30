from agno.agent import Agent
from agno.workflow import Step,Workflow,Parallel
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
# from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv

llm=OpenAIChat(id='gpt-4o-mini')

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")

duckduckgo_agent=Agent(
    name="duckduckgo_agent",
    id="duckduckgo_agent_123",
    model=llm,
    tools=[DuckDuckGoTools()],
    instructions="""
You are a web-search agent that finds current, relevant, and reliable information using DuckDuckGo tools.

Instructions:
- Use DuckDuckGo search whenever the user needs current, external, or uncertain information.
- Write short, targeted search queries.
- Search multiple times if the first results are incomplete or noisy.
- Prefer authoritative, primary, and high-quality sources.
- Verify important facts across more than one result when possible.
- Clearly separate facts from assumptions.
- Do not invent sources, quotes, dates, or statistics.
- If the evidence is weak or conflicting, say so plainly.
- Return a concise summary with the most relevant findings and source links.
"""
)

hackernews_agent=Agent(
    name="hackernews_agent",
    id="hackernews_agent_123",
    model=llm,
    tools=[HackerNewsTools()],
    instructions="""
You are a Hacker News research agent.

Instructions:
- Use Hacker News tools to find relevant posts, threads, comments, and discussion trends.
- Focus on what the community is saying, not just headlines.
- Identify the most relevant posts by recency, engagement, and topical relevance.
- Summarize key points, objections, insights, and patterns from the discussion.
- Distinguish between verified facts and community opinion.
- Do not fabricate titles, links, scores, or comments.
- Return a concise, structured summary with the most important takeaways.
"""
)

reporting_agent=Agent(
    name="reporting_agent",
    id="reporting_agent_123",
    model=llm,
    instructions="""You are the reporting agent. Synthesize only the outputs you receive from the previous workflow step.

Rules:
- Do not search.
- Do not invent missing details.
- Ignore unrelated content.
- If one or both upstream agents found nothing relevant, say that clearly.
- Separate verified web findings from Hacker News discussion.
- Keep the final report short, factual, and directly tied to the user query.
"""
)

duckduckgo_search_step=Step(
    name="duckduckgo_agent_search",
    agent=duckduckgo_agent,
    description="Search the web with DuckDuckGo and return concise, verified findings."
)

hackernews_search_step=Step(
    name="hackernews_agent_search",
    agent=hackernews_agent,
    description="Search Hacker News and summarize the most relevant discussion and trends."
)

reporting_step=Step(
    name="reporting_agent",
    agent=reporting_agent,
     description="Compile and synthesize the outputs from DuckDuckGo and Hacker News into one clear report."
)

parallel_search_agent = Parallel(
    duckduckgo_search_step, hackernews_search_step,
    name="parallel_search_step",
    description="Run DuckDuckGo and Hacker News searches in parallel to gather web results and community discussion."
)

Search_Workflow = Workflow(
    id="search_workflow_123",
    name="search_workflow",
    steps=[parallel_search_agent, reporting_step],
    description="Execute parallel web and Hacker News searches, then synthesize the results into a final report."
)

Search_Workflow.print_response(input="Recent U.S. delegation visit to India",stream=True,markdown=True)

