# ResearchCopilot 🤖📚

### An AI-Powered Multi-Agent Research Assistant

ResearchCopilot is an AI-powered research assistant designed to automate key stages of academic research. It discovers relevant research papers, analyzes their content, generates structured summaries, reviews claims against available evidence, and produces a consolidated research report.

The project uses a multi-agent architecture built with Python, LangGraph, Gemini, and FastAPI.

---

## 🎯 Problem Statement

Academic research often requires researchers and students to spend significant time searching for papers, reading lengthy PDFs, extracting important findings, comparing methodologies, and preparing reports.

ResearchCopilot aims to streamline this process by coordinating specialized AI agents into a single research workflow.

## ✨ Key Features

- **Automated Paper Search:** Finds relevant academic papers using Semantic Scholar.
- **Research Analysis:** Extracts research problems, methodologies, contributions, and findings from available paper content.
- **AI-Powered Summarization:** Produces structured summaries of research papers.
- **Critic Review:** Reviews claims and their supporting evidence within the available research analysis.
- **Report Generation:** Creates a consolidated research report from the preceding agent outputs.
- **Multi-Agent Orchestration:** Coordinates agents through a LangGraph workflow.
- **REST API:** Exposes the research workflow through FastAPI.
- **Web Interface:** Allows users to submit research questions and view results in separate tabs.
- **Automated Testing:** Includes unit and workflow tests.

## 🏗️ Architecture

The research workflow follows these five stages:

```text
                User Research Query
                         |
                         v
                 1. Search Agent
                         |
                         v
                2. Analysis Agent
                         |
                         v
               3. Summarizer Agent
                         |
                         v
                 4. Critic Agent
                         |
                         v
                 5. Writer Agent
                         |
                         v
                 Final Research Report
```

### Agent Responsibilities

| Agent | Responsibility |
|---|---|
| Search Agent | Searches for relevant academic papers and manages search results. |
| Analysis Agent | Extracts and structures research information from available paper content. |
| Summarizer Agent | Generates concise, structured summaries. |
| Critic Agent | Reviews claims against the supplied analysis and evidence. |
| Writer Agent | Produces the consolidated research report. |

**Important limitation:** The Critic Agent does not independently establish the truth of claims. Its review depends on the evidence supplied to it.

## 🛠️ Technology Stack

- **Language:** Python
- **LLM:** Google Gemini
- **Agent Orchestration:** LangGraph
- **Backend:** FastAPI
- **API Server:** Uvicorn
- **Data Validation:** Pydantic
- **Academic Search:** Semantic Scholar API
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** pytest
- **Development Environment:** Visual Studio Code

## 📁 Project Structure

The project is organized into modular components. The following is a high-level overview; retain your actual folder and file names if they differ.

```text
ResearchCopilot/
│
├── app/
│   ├── main.py
│   ├── agents/
│   │   ├── search_agent.py
│   │   ├── analysis_agent.py
│   │   ├── summarizer_agent.py
│   │   ├── critic_agent.py
│   │   └── writer_agent.py
│   │
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── tools/
│   └── workflow/
│
├── config/
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── tests/
├── .env
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python 3.11
- Git (optional, for version control)
- Visual Studio Code
- A Google Gemini API key
- A Semantic Scholar API key if required by your configuration or usage limits

### 1. Clone the repository

If the project is hosted on GitHub:

```bash
git clone YOUR_REPOSITORY_URL
cd ResearchCopilot
```

Alternatively, open your existing project directory in VS Code.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you already have a working virtual environment, you can continue using it.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the API keys expected by your configuration.

Example:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key
```

Replace the example values with your actual keys. Check `config/settings.py` for the exact environment variable names used by your implementation.

**Security:** Never commit `.env` or publish API keys. Add `.env` to `.gitignore`. Keep `.env.example` limited to placeholder values.

## ▶️ Running the Application

Run the commands from the project root, where the `app` and `frontend` folders are located.

### 1. Start the backend

```powershell
python -m uvicorn app.main:app --reload
```

The backend should be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health

### 2. Start the frontend

Open a second PowerShell terminal in the same project directory:

```powershell
python -m http.server 5500 --directory frontend
```

Open the frontend in your browser:

http://127.0.0.1:5500

Keep both terminal windows running while using the application.

## 🧪 Testing

Run the automated tests while excluding tests marked as integration tests:

```powershell
python -m pytest -v -m "not integration"
```

### Current Test Status

The latest recorded regression test run completed with:

- **42 passed**
- **0 failed**
- **3 deselected**
- Runtime: 3.63 seconds

The three deselected tests were excluded by the test marker expression. Test results can change as the code evolves.

## 🔌 API Overview

### Health Check

```http
GET /health
```

Checks the backend health endpoint.

### Research Workflow

```http
POST /api/research
```

Submits a research query to the multi-agent workflow.

The response includes research results such as papers, analyses, summaries, critic reviews, and the final report, according to the API response model.

For the exact request schema and response structure, start the backend and visit:

http://127.0.0.1:8000/docs

## ⚠️ Limitations

- Search quality depends on the availability and relevance of external academic search results.
- External API rate limits, network failures, and timeouts may affect searches.
- Analysis quality depends on the accessible PDF text, abstracts, and language model output.
- Scanned or image-only PDFs may require OCR support.
- AI-generated content can contain errors and should be checked against original papers.
- Critic reviews are limited by the evidence provided to the agent.
- Local development configuration is not a production deployment configuration.

## 🚀 Future Improvements

- Deploy the frontend and backend for remote access.
- Add persistent storage for research history.
- Add PDF upload support and improved document processing.
- Add citation and reference verification.
- Improve retry handling, caching, and API rate-limit management.
- Add user authentication and research project management.
- Add export options for PDF and DOCX reports.
- Improve monitoring, logging, and production error handling.

## 🔐 Responsible Use

ResearchCopilot is intended to assist academic research, not replace careful reading or expert judgment. Verify important claims, citations, methodologies, and conclusions against the original publications before relying on generated reports.

## 👩‍💻 Development

Built as an AI/ML project exploring multi-agent systems, LLM-powered workflows, structured outputs, API development, and automated testing.

---

**ResearchCopilot — From research questions to structured insights.**
