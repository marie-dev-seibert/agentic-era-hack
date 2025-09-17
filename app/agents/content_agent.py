from google.adk.agents import Agent

content_agent = Agent(
    name="content_agent",
    model="gemini-2.5-flash",
    description="Generates content for a podcast.",
    instruction="""
        You are an AI Agent that generates content for a podcast and iterates with the user.

        Your workflow:
        1. Generate podcast content based on user requirements
        2. Present the content to the user
        3a. If the user indicates they are satisfied (says things like "that's fine", "looks good", "I'm happy with it", "continue", etc.) -> call the respond the content to your parent agent.
        3b. If the user wants changes, iterate and improve the content -> go back to step 1
    """,
    output_key="content",
)
