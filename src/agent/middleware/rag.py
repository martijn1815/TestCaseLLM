from typing import Any
from langchain_core.documents import Document
from langchain.agents.middleware import AgentMiddleware, AgentState

from src.database.vectorstore import vector_store
from src.agent.prompts import RAG_PROMPT


class State(AgentState):
    context: list[Document]


class RetrieveDocumentsMiddleware(AgentMiddleware[State]):
    state_schema = State

    def before_model(self, state: AgentState) -> dict[str, Any] | None:
        """
        2-Step RAG, the retrieval step is always executed before the generation step.
        This architecture is straightforward and predictable, making it suitable for many applications
        where the retrieval of relevant documents is a clear prerequisite for generating an answer.
        :param state:
        :return:
        """
        last_message = state["messages"][-1]
        retrieved_docs = vector_store.similarity_search(last_message.text, 3)

        docs_content = "\n\n".join(
            f"'''\nDocument Name:\n{doc.metadata['file_name']}\n\nDocument Content:\n{doc.page_content}'''"
            for doc in retrieved_docs
        )

        augmented_message_content = (
            f"{last_message.text}\n\n"
            f"{RAG_PROMPT}\n"
            f"{docs_content}"
        )
        return {
            "messages": [last_message.model_copy(update={"content": augmented_message_content})],
            "context": retrieved_docs,
        }

RAG = RetrieveDocumentsMiddleware()
