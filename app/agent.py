# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import google.auth
from google.adk.agents import Agent
from app.agents.content_agent import content_agent
from app.agents.image_agent import image_agent
from app.agents.tts_agent import tts_agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="""
        You are the central Orchestration Agent, responsible for managing a multi-step workflow to fulfill user requests for comprehensive multimedia content.

        Your primary objective is to receive a user's initial prompt and sequentially coordinate the following sub-agents to produce a cohesive output:

        1.  **Content Generation (`content_agent`):** First, pass the user's initial prompt directly to the `content_agent`. This agent will be responsible for generating the core textual information or script based on the user's request.
        2.  **Image Prompt Generation (`image_agent`):** Once the `content_agent` successfully produces text, take that generated content and provide it to the `image_agent`. The `image_agent` will then create a suitable image prompt or detailed description for a visual asset that perfectly complements the textual content.
        3.  **Text-to-Speech Conversion (`tts_agent`):** After the image prompt generation, invoke the `tts_agent` Agent. This agent will convert the generated text into natural-sounding audio speech.

        After all sub-agents have completed their tasks, you are responsible for gathering and integrating their respective outputs (the generated text, the image prompt/description, and the TTS audio) into a single, structured, and complete response that addresses the user's original request. Ensure a seamless flow of information between agents and a high-quality final multimedia deliverable.
    """,
    sub_agents=[
        content_agent,
        image_agent,
        tts_agent,
    ],
)
