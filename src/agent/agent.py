from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

from src.config.settings import settings
from src.agent.models import ResponseFormat
from src.agent.prompts import SYSTEM_PROMPT


model = ChatOllama(
    model=settings.model,
    base_url=settings.host_url,
    temperature=0
)

# In production a persistent checkpointer should be used.
checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

def get_response(thread_id: str, prompt: str) -> ResponseFormat:
    # `thread_id` is a unique identifier for a given conversation.
    config = {"configurable": {"thread_id": thread_id}}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config
    )

    return response['structured_response']


if __name__ == '__main__':
    print(get_response(thread_id="1", prompt="Can you tell me a joke?").response)
