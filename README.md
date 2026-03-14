# Legacy Code Explainer

An intelligent AI-powered assistant designed to help developers migrate, refactor, and understand legacy codebases. Leveraging RAG (Retrieval-Augmented Generation) and web search capabilities, the app acts as a technical advisor that identifies critical issues, highlights security vulnerabilities, and generates step-by-step modernization plans.

## Features
- **Codebase Indexing:** Upload your legacy `.py`, `.java`, `.cob`, `.js`, or other code files, and the app automatically indexes them for specific querying.
- **Dual Response Modes:** Choose between **Concise** summaries or **Detailed** architectural analyses.
- **Web Search Integration:** Automatically searches for known CVEs or modern alternatives when the local codebase doesn't have the answer.
- **Technical Debt Logging:** Silently logs critical issues and migration plans identified during the chat into an SQLite database for project managers.
- **Admin Dashboard:** A dedicated UI page to view and manage accumulated technical debt logs across sessions.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

Start the Streamlit app:
```bash
streamlit run app.py
```

### Testing the App
**Dummy Data Included:** There is dummy testing data included directly inside this GitHub repository folder. Feel free to use the provided sample legacy code files to test the indexing, AI explanations, and technical debt extraction features!

## Architecture
- **Frontend:** Streamlit
- **LLM/Orchestration:** LangChain & Groq (Llama-3.1-8b)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
- **Vector Store:** FAISS
- **Database Logs:** SQLite + Pandas
