import os
from collections.abc import AsyncGenerator

import google.auth
from google.adk.agents import BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.tools.agent_tool import AgentTool

from app.agents.content_agent import content_agent
from app.agents.human_review_agent import (
    human_review_content_agent,
    human_review_image_agent,
)
from app.agents.image_agent import image_agent
from app.agents.tts_agent import tts_agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


# Custom agent to check if user approved the content
class ContentApprovalChecker(BaseAgent):
    """Checks if user approved the content and decides next step."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Check the review result from content human review agent
        review_result = ctx.session.state.get("content_review_result")

        if not review_result:
            # No review result found, continue the loop
            yield Event(author=self.name)
            return

        # Extract status from the structured review result
        status = review_result.get("status", "edit")

        if status == "approved":
            # User approved, escalate to stop the loop and move to next agent
            yield Event(author=self.name, actions=EventActions(escalate=True))
        elif status == "cancel":
            # User wants to cancel, escalate to stop the loop
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:  # status == "edit"
            # User wants changes, continue the loop
            yield Event(author=self.name)


# Custom agent to check if user approved the image
class ImageApprovalChecker(BaseAgent):
    """Checks if user approved the image and decides next step."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Check the review result from image human review agent
        review_result = ctx.session.state.get("image_review_result")

        if not review_result:
            # No review result found, continue the loop
            yield Event(author=self.name)
            return

        # Extract status from the structured review result
        status = review_result.get("status", "edit")

        if status == "approved":
            # User approved, escalate to stop the loop and move to next agent
            yield Event(author=self.name, actions=EventActions(escalate=True))
        elif status == "cancel":
            # User wants to cancel, escalate to stop the loop
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:  # status == "edit"
            # User wants changes, continue the loop
            yield Event(author=self.name)


# Create iterative workflows for content and image generation
content_refinement_loop = LoopAgent(
    name="content_refinement_loop",
    sub_agents=[
        content_agent,
        human_review_content_agent,
        ContentApprovalChecker(name="content_approval_checker"),
    ],
    max_iterations=3, # Prevent infinite loops
    description="Iteratively refines content until user approves",
)

image_refinement_loop = LoopAgent(
    name="image_refinement_loop",
    sub_agents=[
        image_agent,
        human_review_image_agent,
        ImageApprovalChecker(name="image_approval_checker"),
    ],
    max_iterations=3, # Prevent infinite loops
    description="Iteratively refines image until user approves",
)

# Main coordinator workflow
# coordinator_agent = SequentialAgent(
#     name="coordinator_agent",
#     sub_agents=[
#         content_refinement_loop,  # Step 1: Content with iterative refinement
#         image_refinement_loop,  # Step 2: Image with iterative refinement
#         tts_agent,  # Step 3: Final TTS generation
#     ],
#     description="Orchestrates podcast creation with iterative refinement",
# )

content_tool = AgentTool(agent=content_agent)
image_tool = AgentTool(agent=image_agent)

coordinator_agent = LoopAgent(
    name="coordinator_agent",
    sub_agents=[
        content_refinement_agent,  # Step 1: Content with iterative refinement
        image_refinement_loop,  # Step 2: Image with iterative refinement
        tts_agent,  # Step 3: Final TTS generation
    ],
    description="Orchestrates podcast creation with iterative refinement",
)