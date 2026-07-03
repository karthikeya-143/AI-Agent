# Agentic AI Assistant

![Agentic AI Assistant Banner](assets/agent-banner.svg)

An intelligent AI assistant built with Streamlit and LangChain that can answer user queries by combining web search with live weather information.

## Overview

This project demonstrates how an agent can use multiple tools to solve a task in a single flow. The assistant accepts a user question, searches the web for relevant context, and can also fetch weather details for a city when needed.

## Features

- Interactive Streamlit web UI
- Agent-based reasoning using LangChain
- Web search integration via Tavily
- Weather lookup using Weatherstack
- Simple setup with Python environment files

## Project Workflow

1. User enters a query in the Streamlit interface.
2. The app sends the request to the LangChain agent.
3. The agent decides which tool is needed:
   - Use web search for general information
   - Use the weather tool for current weather questions
4. The selected tool returns data to the agent.
5. The agent combines the results and generates a final response.
6. The final answer is displayed in the UI for the user.

## Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini
- Tavily Search API
- Weatherstack API

## Setup Instructions

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

## Built with Love ❤️

Developed by Karthikeya