from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.workflow import Step,Workflow

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")
llm=OpenAIChat(id='gpt-4o-mini')

EssayAgent=Agent(
    id="essay-agent-123",
    name="Essay-Agent",
    model=llm,
    instructions="""
    - You are an expert essay writing agent.
    - Write clear, well-structured, and grammatically correct essays.
    - Expand the user's idea into a complete essay with an introduction, body, and conclusion when appropriate.
    - Maintain the tone requested by the user: formal, persuasive, descriptive, analytical, narrative, or reflective.
    - Improve clarity, coherence, and flow without changing the core meaning.
    - Use strong transitions and logical paragraph structure.
    - If the user provides a topic only, create a complete essay from it.
    - If the user provides a draft, refine and rewrite it into a polished essay.
    - Keep the response focused on essay writing only.
    """
)

ExtractionAgent=Agent(
    id="extraction-agent-123",
    name="Extraction-Agent",
    model=llm,
    instructions="""
    - You are an information extraction agent.
    - Extract only the requested information from the provided text.
    - Do not add extra commentary, opinions, or unrelated details.
    - Preserve the original meaning exactly.
    - Return the result in a clean, structured format when helpful.
    - If the user asks for names, dates, entities, key points, tasks, or facts, extract them precisely.
    - If the user asks for a summary of extracted items, keep it brief and accurate.
    - If the input is ambiguous, infer the most likely extraction format from the request.
    - Keep the response concise and factual.
    """
)

essay_writing_steps=Step(
    name="Essay_Writing",
    agent=EssayAgent,
    description="Generate an Essay based on a Topic"
)

extraction_steps=Step(
    name="Extraction_step",
    agent=ExtractionAgent,
    description="Extract important points based on the Paragraph created in the above step"
)

information_workflow=Workflow(
    name="essay_extraction_workflow",
    id="essay_extraction_workflow_123",
    steps=[essay_writing_steps,extraction_steps],
    description="A workflow that first generates or refines essay content, then extracts key information from the result or related text. It combines creative writing and structured information extraction in a single pipeline."
)

information_workflow.print_response(input="Write a Paragraph on Topic India",stream=True,markdown=True)




