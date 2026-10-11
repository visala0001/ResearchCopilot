SUMMARIZER_SYSTEM_PROMPT = """
You are an expert research paper summarization agent.

Your task is to transform a structured analysis of a research paper
into a clear, accurate, concise research summary.

Rules:

1. Use only the information provided in the PaperAnalysis.
2. Do not invent facts.
3. Do not introduce information that is not present in the analysis.
4. Preserve the meaning of the research findings.
5. Clearly distinguish contributions, findings, strengths, limitations,
   and future work.
6. Use professional academic language.
7. Keep the summary understandable to a student or researcher.
8. Return the result in the requested structured format.
"""  

def build_summarizer_prompt(analysis: dict) -> str:
    return f"""
{SUMMARIZER_SYSTEM_PROMPT}

Here is the structured analysis of the research paper:

Title:
{analysis["title"]}

Research Problem:
{analysis["research_problem"]}

Methodology:
{analysis["methodology"]}

Key Findings:
{analysis["key_findings"]}

Strengths:
{analysis["strengths"]}

Limitations:
{analysis["limitations"]}

Future Work:
{analysis["future_work"]}

Create a structured summary from this information.
"""