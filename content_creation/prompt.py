initial_prompt = """
Write a complete {type} audio script that strictly follows the user's inputs and constraints.

Constraints:
- Chapter length: {chapter_length}.
- Language: write everything in {language}.
- Length: {length}.
- Format: {format}. Structure the episode with a clear beginning, multiple chapters, and an outro.
- Speakers: {speakers}.
- Audience: {target_audience}, ages {target_age}. Use a friendly, engaging, age-appropriate tone.
- Core objective: {core_objective}.
- Topics to cover: {topics}.
- Keywords to weave in naturally: {keywords}.

Deliverable:
1) Metadata header (concise):
   - Title:
   - One-sentence description:
   - Target audience:
   - Estimated duration:
   - Keywords:
   - Topics:

2) Scripted episode (ready to record):
   - Cold open hook (1–2 sentences) [SFX: intro sting]
   - Show intro and host greeting
   - Chapter 1: clear subheading, learning goal, main content, 1 interactive question/activity
   - Chapter 2: clear subheading, learning goal, main content, 1 interactive question/activity
   - Chapter 3: clear subheading, learning goal, main content, 1 interactive question/activity
   - Fun fact segment (kid-friendly)
   - Recap of key points
   - Call-to-action (age-appropriate)
   - Outro and credits

Writing guidelines:
- Keep sentences short and vocabulary simple; briefly explain any complex term in kid-friendly language.
- Use stage directions in square brackets (e.g., [SFX: gentle music], [PAUSE], [HOST], [CO-HOST]).
- Smooth transitions between chapters; avoid abrupt topic changes.
- Be inclusive and positive; avoid sensitive or unsafe content.
- If any input is missing, make reasonable, child-safe assumptions consistent with the objective.

Sources:
- If you present specific facts, add a "Sources" section at the end with 2–3 reputable references.

Return only the script content described above, with the headers indicated, and no extra commentary.
"""

# rendered_prompt = prompt.format(
#     language=language,
#     format=format,
#     target_audience=target_audience,
#     target_age=target_age,
#     core_objective=core_objective,
#     topics=topic,
#     keywords=", ".join(keywords),
#     type=type,
# )

# print(rendered_prompt)