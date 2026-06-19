"""
ReAct agent setup for document retrieval and question answering.
"""

import os

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.config.settings import Config
from src.llms.openai import llm
from src.rag.retriever_setup import get_retriever

config = Config()

# Initialize tools
tools = [get_retriever()]

# Load document description if available
if os.path.exists("description.txt"):
    with open("description.txt", "r", encoding="utf-8") as f:
        description = f.read()
else:
    description = None

# Create Tool Calling agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", config.prompt("system_prompt")),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Initialize the Tool Calling agent and executor
react_agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=react_agent,
    tools=tools,
    handle_parsing_errors=True,
    max_iterations=10,
    verbose=True,
    return_intermediate_steps=True
)
