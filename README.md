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

### Example Questions

Once you have uploaded a sample file and indexed it, try asking the chatbot questions like the ones below.

---

#### 🖥️ Python Sample (`legacy_emp_data.py`)

> *"What does the `do_everything` function do, and why is it considered bad practice?"*

> *"Are there any security vulnerabilities in this code? Identify them and explain the risks."*

> *"The authentication uses MD5 hashing — is that still secure? What should I replace it with?"*

> *"This code appears to have a SQL injection vulnerability. Can you show me how to fix it using parameterized queries?"*

> *"What is the export path hardcoded in this file, and why is hardcoding file paths a problem in production?"*


---

#### 🖥️ COBOL Sample (`payroll_report.cob`)

> *"What does this COBOL program do? Give me a plain-English explanation."*

> *"How is overtime pay calculated in this program? What is the overtime threshold?"*

> *"What are the file I/O operations being performed, and what files does this program read from and write to?"*

> *"How would I migrate this COBOL payroll logic to a modern Python or Java equivalent?"*


## Response Modes

The bot supports two response modes, toggled from the sidebar.

### ⚡ Concise Mode
Structured snapshot for quick triage. Every response includes:
- **Risk Level** — High / Medium / Low
- **Summary** — One sentence on what the code does
- **Critical Issues** — Up to 3 key problems found
- **Migration Action Plan** — One-sentence next step

### 🔍 Detailed Mode
Full architectural breakdown for planning a migration. Every response includes:
- **What It Does** — Plain-English explanation of the code
- **Security & Risk Analysis** — Vulnerabilities, CVEs, and deprecated patterns
- **What Breaks If Removed/Changed** — Dependent functions or behaviours
- **Modern Alternatives** — Specific libraries or frameworks to replace legacy code
- **Step-by-Step Migration Plan** — Numbered, actionable developer tasks

---

## Architecture
- **Frontend:** Streamlit
- **LLM/Orchestration:** LangChain & Groq (Llama-3.1-8b)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
- **Vector Store:** FAISS
- **Database Logs:** SQLite + Pandas
