from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import Step,Workflow,Condition,StepInput
from dotenv import load_dotenv

load_dotenv("/Users/nilasark/experiments/agno-learning/.env")
llm=OpenAIChat("gpt-4o-mini")

def review_email(input_step:StepInput)->bool:
    topic=input_step.previous_step_content
    if topic:
        topic=topic.lower()
        if "subject" in topic:
            return True
        return False
    return False


email_draft_agent=Agent(
    id="email_draft_agent_123",
    name="email_draft_agent",
    model=llm,
    markdown=True,
    instructions="""
You draft clear, professional email content based on the user's intent and available context.
Write concise, natural-sounding emails with an appropriate tone for the recipient and situation.
Preserve any specific names, dates, facts, and action items provided by the user.
If the request is ambiguous, make the safest reasonable assumption and keep the draft broadly usable.
Return only the email draft content, without explanations or metadata.
"""
)

email_output_agent=Agent(
    id="email_output_step_123",
    name="email_output_step"
)

email_draft_step = Step(
    name="email_draft_step",
    agent=email_draft_agent,
    description="Drafts the email body from the user's request and context."
)

email_output_step = Step(
    name="email_output_step",
    agent=email_output_agent,
    description="Formats the final email output for delivery or review."
)

email_review_step = Condition(
    name="email_review_step",
    steps=[email_output_step],
    evaluator=review_email,
    description="Evaluates the drafted email and routes it based on review outcome."
)

email_generation_workflow = Workflow(
    id="email_generation_workflow_123",
    name="email_generation_workflow",
    steps=[email_draft_step, email_review_step],
    description="Generates an email draft and runs it through a review gate before final output."
)

email_generation_workflow.print_response(input="Topic:One day leave to Manager",stream=True,markdown=True)

