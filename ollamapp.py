import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("user", "Question:{question}")
    ]
)

st.set_page_config(page_title="SOM TRICHY", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        font-family: 'Montserrat', sans-serif;
        color: white;
        margin: 0;
        padding: 0;
    }

    .stApp {
        animation: fadeIn 2s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .title {
        font-size: 50px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        text-shadow: 2px 2px 10px #ffcc00;
        animation: fadeIn 1s ease-out;
    }

    .subtitle {
        font-size: 20px;
        color: #f5f5f5;
        text-align: center;
        margin-bottom: 40px;
        text-shadow: 1px 1px 5px #ffffff;
        animation: fadeIn 1.5s ease-in-out;
    }

    .input-box {
        margin: 20px auto;
        text-align: center;
    }

    .input-field {
        width: 60%;
        padding: 15px;
        font-size: 18px;
        border-radius: 25px;
        border: 2px solid #ffcc00;
        outline: none;
        background: rgba(0, 0, 0, 0.7);
        color: #ffffff;
        box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease-in-out;
    }

    .input-field:focus {
        box-shadow: 0px 6px 15px rgba(255, 204, 0, 0.7);
        background: rgba(0, 0, 0, 0.9);
    }

    .response-box {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        max-width: 800px;
        margin: 20px auto;
        animation: fadeIn 1.2s ease-out;
    }

    .footer {
        font-size: 16px;
        color: #ffffff;
        text-align: center;
        margin-top: 40px;
        padding-right: 20px;
        animation: fadeIn 3s ease-in-out;
    }

    .footer a {
        color: #ffcc00;
        text-decoration: none;
    }

    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🤖CHATBOT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask any question, and I’ll provide a helpful answer.</div>', unsafe_allow_html=True)

if "response" not in st.session_state:
    st.session_state.response = ""

def handle_input():
    user_input = st.session_state["user_input"]
    if user_input.strip():
        llm = OllamaLLM(model="gemma:2b")
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        with st.spinner("Processing your question..."):
            response = chain.invoke({"question": user_input})
        st.session_state.response = response
        st.session_state.user_input = ""

st.markdown('<div class="input-box">', unsafe_allow_html=True)
st.text_input(
    label="",
    placeholder="Type your question here and press Enter...",
    key="user_input",
    on_change=handle_input
)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.response:
    st.markdown('<div class="response-box">', unsafe_allow_html=True)
    st.write(st.session_state.response)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
            
    </div>
    """,
    unsafe_allow_html=True
)
