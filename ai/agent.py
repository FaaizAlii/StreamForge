from typing import TypedDict

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from ai.ai_tools import TOOLS


class AgentContext(TypedDict):
    user_id: int


llm = ChatOllama(
    model="qwen3.5:4b",
    temperature=0,
)


SYSTEM_PROMPT = """
You are the StreamForge AI support assistant.

You help authenticated StreamForge customers with:

- Their account information
- Their subscription
- Movies and shows
- Searching movies and shows
- Searching movies and shows by genre
- Movie and show details

Use tools whenever the user's question requires information
from the StreamForge database.

Never invent database information.

You are helping the currently authenticated customer.
Never ask the customer for their user ID.

If a tool returns no results, clearly tell the user that
nothing was found.

Keep responses concise and helpful.
"""


agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    context_schema=AgentContext,
)