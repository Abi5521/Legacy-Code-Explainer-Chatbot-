import streamlit as st
import logging

from utils.document_processor import process_uploaded_file
from utils.rag_utils import get_vectorstore, get_retriever
from utils.legacy_advisor import get_agent_executor
from utils.db_logger import log_technical_debt, clear_technical_debt
from models.embeddings import get_embeddings
from models.llm import get_llm

from langchain_core.messages import HumanMessage, AIMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Legacy Code Explainer", page_icon="🤖", layout="wide")

def instructions_page():
    st.title("📖 Instructions")
    st.markdown("""
    ### Welcome to the Legacy Code Explainer!
    
    This application allows you to upload legacy codebase files and ask questions about them.
    
    **How to use:**
    1. Navigate to the **Chat** page using the sidebar.
    2. Upload your legacy code files (e.g., `.py`, `.java`, `.cob`, `.js`). The codebase will be indexed automatically.
    3. Start asking questions! You can toggle between **Concise** and **Detailed** responses.
    
    If the bot cannot find the answer in your uploaded code, it will automatically search the web for modern migration guides or best practices.
    """)

def admin_page():
    st.title("Technical Debt Log")
    st.markdown("This page displays technical debt identified by the AI across all chat sessions.")
    
    try:
        import sqlite3
        import pandas as pd
        
        conn = sqlite3.connect("admin_logs.db")
        df = pd.read_sql_query("SELECT timestamp, issues_identified, migration_plan FROM technical_debt ORDER BY id DESC", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("Timestamp", width="small"),
                    "issues_identified": st.column_config.TextColumn("Issues Identified", width="large"),
                    "migration_plan": st.column_config.TextColumn("Migration Plan", width="large"),
                }
            )
            
            if st.button("🗑️ Clear Log", use_container_width=True):
                clear_technical_debt()
                st.rerun()
        else:
            st.info("No technical debt logged yet.")
            
    except Exception as e:
        st.error("Could not load database. Make sure you have chatted with the bot first to generate logs.")
        logger.error(f"Error loading admin page: {e}")

def chat_page():
    st.title("🤖 Legacy Code Chat")
    st.markdown("Upload your legacy code and ask questions about it, or get migration advice. The app uses web search if it doesn't know the answer directly.")

    uploaded_files = st.file_uploader(
        "Upload Legacy Files (.py, .js, .java, etc.)", 
        accept_multiple_files=True,
        type=None
    )
    
    if uploaded_files:
        current_files_signature = "-".join([f"{f.name}-{f.size}" for f in uploaded_files])
        if st.session_state.get("indexed_files_signature") != current_files_signature:
            with st.spinner("Processing documents..."):
                all_chunks = []
                for file in uploaded_files:
                    chunks = process_uploaded_file(file)
                    all_chunks.extend(chunks)
                    
                if all_chunks:
                    embeddings = get_embeddings()
                    if embeddings:
                        vectorstore = get_vectorstore(all_chunks, embeddings)
                        if vectorstore:
                            st.session_state["retriever"] = get_retriever(vectorstore)
                            st.session_state["indexed_files_signature"] = current_files_signature
                            st.success("Codebase successfully indexed!")
                        else:
                            st.error("Failed to create vector store. Check logs.")
                    else:
                        st.error("Failed to initialize embeddings model.")
                else:
                    st.error("Failed to extract text from files.")

    with st.sidebar:
        st.divider()
        st.header("Chat Settings")
        mode_toggle = st.radio(
            "Response Mode:",
            ["Concise", "Detailed"],
            index=0,
            horizontal=False,
            help="Concise: Short, summarized replies. Detailed: In-depth response."
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def render_message(role, content):
        with st.chat_message(role):
            if role == "user" and "\n" in content:
                st.code(content, language=None)
            else:
                st.markdown(content)

    for message in st.session_state.messages:
        render_message(message["role"], message["content"])

    prompt = st.chat_input("Ask about your code or how to migrate it...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_message("user", prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                retriever = st.session_state.get("retriever", None)
                llm = get_llm()
                
                if llm:
                    agent_executor = get_agent_executor(llm, retriever, mode_toggle)
                    if agent_executor:
                        try:
                            chat_history = []
                            for msg in st.session_state.messages[:-1]:
                                if msg["role"] == "user":
                                    chat_history.append(HumanMessage(content=msg["content"]))
                                elif msg["role"] == "assistant":
                                    chat_history.append(AIMessage(content=msg["content"]))
                                    
                            response = agent_executor.invoke({
                                "messages": chat_history + [HumanMessage(content=prompt)]
                            })
                            
                            output = response["messages"][-1].content
                            
                            log_technical_debt(output)
                            
                            st.markdown(output)
                            st.session_state.messages.append({"role": "assistant", "content": output})
                        except Exception as e:
                            st.error(f"Error executing agent: {e}")
                    else:
                        st.error("Could not initialize agent. Check logs.")
                else:
                    st.error("Could not initialize LLM. Make sure GROQ_API_KEY is set in .env.")

def main():
    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions", "Technical Debt Log"],
            index=0
        )
        
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    if page == "Instructions":
        instructions_page()
    elif page == "Chat":
        chat_page()
    elif page == "Technical Debt Log":
        admin_page()

if __name__ == "__main__":
    main()