import os
import requests
import streamlit as st
import certifi
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub

from langchain_community.tools.tavily_search import TavilySearchResults

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ==========================================
# STREAMLIT PAGE CONFIG
# ==========================================


st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main { padding-top: 0.5rem; }
    .hero-card {
        background: linear-gradient(135deg, #0f172a, #1d4ed8);
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        color: white;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.2);
        margin-bottom: 1rem;
    }
    .hero-card h1 {
        margin-bottom: 0.2rem;
        font-size: 2rem;
    }
    .hero-card p {
        font-size: 1rem;
        opacity: 0.95;
    }
    .info-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
    }
    .stTextInput > div > div > input {
        border-radius: 12px;
        padding: 0.7rem 0.8rem;
    }
    .stButton > button {
        border-radius: 999px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        border: none;
    }
    .result-card {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-left: 5px solid #2563eb;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-top: 0.8rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
    }
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 1.8rem;
        padding: 0.8rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1>🤖 Agentic AI Assistant</h1>
        <p>Ask one question and let the agent combine smart web search with live weather insights.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="info-card">
            <b>✨ What it can do</b><br>
            Search the web for useful information and fetch current weather for a city in one flow.
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="info-card">
            <b>💡 Example prompt</b><br>
            “Find the capital of India and current weather there.”
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(max_results=2)

# ==========================================
# WEATHER TOOL
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"http://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

# ==========================================
# PROMPT
# ==========================================

prompt = hub.pull("hwchase17/react")

# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]

# ==========================================
# CREATE AGENT
# ==========================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ==========================================
# EXECUTOR
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ==========================================
# UI INPUT
# ==========================================

st.markdown("### Ask your agent")
user_query = st.text_input(
    "",
    placeholder="Example: Find the capital of India and current weather"
)

# ==========================================
# RUN AGENT
# ==========================================

if st.button("Run Agent", use_container_width=True):

    if user_query:

        with st.spinner("Agent is thinking..."):

            try:
                response = agent_executor.invoke({
                    "input": user_query
                })

                st.success("Response Generated")
                st.markdown(
                    """
                    <div class="result-card">
                        <h3>Final Response</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.write(response["output"])

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.warning("Please enter a query")

st.markdown(
    """
    <div class="footer">Developed by Karthikeya</div>
    """,
    unsafe_allow_html=True,
)