import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Train Groq to return only the translated text
system_template = "Translate the following into {language}. Provide only the translated text and nothing else."
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)
parser = StrOutputParser()

st.set_page_config(page_title="CRB", page_icon="🌍", layout="wide")

# CSS styling for a professional look
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #1f1f1f, #000000);
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
        font-size: 60px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        text-shadow: 3px 3px 15px #1e90ff;
        animation: fadeIn 1s ease-out;
    }

    .subtitle {
        font-size: 20px;
        color: #f0f0f0;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 10px #ffffff;
        animation: fadeIn 1.5s ease-in-out;
    }

    .translator-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        max-width: 1000px;
        margin: 30px auto;
        padding: 40px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.7);
    }

    .text-area {
        width: 45%;
        padding: 15px;
        font-size: 18px;
        border-radius: 15px;
        border: 1px solid #ffffff;
        background-color: rgba(0, 0, 0, 0.9);
        color: white;
        resize: none;
        height: 200px;
        box-shadow: inset 0px 4px 8px rgba(255, 255, 255, 0.1);
    }

    .text-area:focus {
        outline: none;
        border-color: #00bfff;
        box-shadow: 0px 0px 15px #00bfff;
    }

    .select-box {
        width: 100%;
        margin: 10px 0;
        padding: 10px;
        font-size: 16px;
        border-radius: 10px;
        border: 1px solid #ffffff;
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
    }

    .translate-button {
        background-color: #1e90ff;
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 10px;
        cursor: pointer;
        text-transform: uppercase;
        margin-top: 20px;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.5);
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    .translate-button:hover {
        background-color: #00bfff;
        transform: scale(1.05);
    }

    .footer {
        font-size: 16px;
        color: white;
        text-align: center;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown('<div class="title">🌍 CRB Language Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Effortless translation made simple and professional</div>', unsafe_allow_html=True)

# Translator UI
st.markdown('<div class="translator-container">', unsafe_allow_html=True)

# Input Text Area
col1, col2 = st.columns(2, gap="large")

with col1:
    st.selectbox("Input Language:", ["English", "Tamil", "Malayalam", "Hindi"], key="input_lang")
    st.text_area(
        "Input Text:",
        key="input_text",
        placeholder="Type your text here...",
        height=200,
        label_visibility="collapsed"
    )

with col2:
    st.selectbox("Output Language:", ["English", "Tamil", "Malayalam", "Hindi"], key="output_lang")
    st.text_area(
        "Translated Text:",
        value=st.session_state.output_text if "output_text" in st.session_state else "",
        height=200,
        disabled=True,
        label_visibility="collapsed"
    )

# Translate button
if st.button("Translate", key="translate_button", help="Click to translate the text.", use_container_width=True):
    chain = prompt_template | model | parser
    try:
        st.session_state.output_text = chain.invoke({
            "text": st.session_state.input_text,
            "language": st.session_state.output_lang
        })
    except Exception as e:
        st.session_state.output_text = f"Error: {str(e)}"

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Powered by CRB Language Translator</div>', unsafe_allow_html=True)
