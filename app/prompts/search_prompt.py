SEARCH_QUERY_PROMPT = """
You are an academic research search assistant.

Given a research question, generate 3 to 5 concise search queries
that can be used to find relevant academic papers.

Requirements:
- Preserve the main research topic.
- Use different useful terminology or perspectives.
- Prefer academic terminology.
- Do not answer the research question.
- Return only the search queries.
- Do not number them.
- One query per line.

Research question:
{query}
"""