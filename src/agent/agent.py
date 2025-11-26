from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

from src.config.settings import settings
from src.agent.models import ResponseFormat
from src.agent.prompts import SYSTEM_PROMPT
from src.agent.middleware.rag import RAG


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
    checkpointer=checkpointer,
    middleware=[RAG]
)


def get_response(thread_id: str, prompt: str) -> ResponseFormat:
    """
    Receive thread id (unique identifier for a given conversation) and prompt message,
    then invoke a response from the agent. Returns the structured response.
    :param thread_id: unique identifier for a given conversation
    :param prompt:
    :return ResponseFormat:
    """

    config = {"configurable": {"thread_id": thread_id}}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config
    )

    return response['structured_response']


if __name__ == '__main__':
    from src.database.vectorstore import ingest_md_files, vector_store
    ingest_md_files()
    print(vector_store.similarity_search("Can I use my own equipment?"))
    print(get_response(thread_id="1", prompt="Can I use my own equipment?").response)
