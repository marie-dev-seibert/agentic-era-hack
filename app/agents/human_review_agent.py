from typing import Literal

from google.adk.agents import Agent
from google.adk.tools.get_user_choice_tool import get_user_choice_tool
from pydantic import BaseModel, Field

class ReviewResult(BaseModel):
    """Model for human review feedback on podcast content."""
    status: Literal["approved", "edit", "cancel"] = Field(
        description="Review decision: 'approved' if content is ready, 'edit' if changes needed, 'cancel' if content should be abandoned"
    )
    description: str = Field(
        description="Detailed explanation what the user wants to do with the content/image"
    )

human_review_content_agent = Agent(
    name="content_human_reviewer",
    model="gemini-2.5-flash",
    instruction="""
    You are an AI Agent guiding a human through the review process of podcast content.

    Ask the user for their opinion on the content and if they want to edit anything.
    """,
    description="Human-in-the-loop reviewer for podcast content",
    tools=[get_user_choice_tool],
)

human_review_image_agent = Agent(
    name="image_human_reviewer",
    model="gemini-2.5-flash",
    instruction="""
    You are an AI Agent guiding a human through the review process of podcast image.

    Ask the user for their opinion on the image and if they want to edit anything.
    """,
    description="Human-in-the-loop reviewer for podcast image",
    tools=[get_user_choice_tool],
)
