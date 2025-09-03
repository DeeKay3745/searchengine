import streamlit as st
import logging
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities  import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.tools import DuckDuckGoSearchRun
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
# keep your existing QRoQ setup / imports here
# (assuming you already defined your custom model code above this part)

#groq_api_key = os.getenv("GROQ_API_KEY")
tools = []

# Safe import for DuckDuckGo
try:
    from langchain_community.tools import DuckDuckGoSearchRun
    search = DuckDuckGoSearchRun(name="Search")
    tools.append(search)
except ImportError as e:
    logging.warning(f"DuckDuckGoSearchRun not available: {e}")
except Exception as e:
    logging.warning(f"Unexpected error loading DuckDuckGoSearchRun: {e}")

# Initialize your QRoQ model (sticking to your original code)
#llm = ChatOpenAI(
#    model="gpt-3.5-turbo", 
#    api_key=api_key,  # ⚡ keep your model here (update if QRoQ alias differs)
#    temperature=0
#)
##sidebar for settings
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv =ArxivQueryRun(api_wrapper = arxiv_wrapper)

api_wrapper  = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

search =DuckDuckGoSearchRun(name = "Search")
st.title("Langchain -Chat with Search")
"""
In this example, we're using 'StreamlitCallbackHandler' to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more Langchain streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""
st.sidebar.title("Settings")
groq_api_key = st.sidebar.text_input("Enter your Groq api key:", type = "password")

llm =ChatGroq(groq_api_key= groq_api_key, model_name="llama-3.1-8b-instant", streaming=True)
# Initialize the agent
tools = [search,arxiv,wiki]
search_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True   # ✅ prevents crashes on parsing
)

# Streamlit UI code stays the same
st.title("QRoQ + Search Agent")
user_input = st.text_input("Ask me something:")

if user_input:
    response = search_agent.run(user_input)
    st.write(response)