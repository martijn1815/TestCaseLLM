from langchain.agents.middleware import wrap_model_call, ModelResponse
from langchain.messages import AIMessage

from src.database.vectorstore import vector_store
from src.agent.models import ResponseFormat


@wrap_model_call
def validate_docs(request, handler):
    """
    Hallucination check: Validate if the returned documents exist in the database.
    :param request:
    :param handler:
    :return response:
    """
    response = handler(request)

    # No related file is found/implemented by the Agent:
    if not response.structured_response:
        content_overwrite = "I am sorry I could not find any information related to your question."
        return ModelResponse(
            result=[AIMessage(content=content_overwrite)],
            structured_response=ResponseFormat(response=content_overwrite, documents=[]),
        )

    # Check if documents have been hallucinated:
    docs_in_agent_output = [x.lower() for x in response.structured_response.documents]
    docs_in_vectorstore = [x["metadata"]["file_name"].lower() for x in vector_store.store.values()]
    docs_hallucinated = [doc for doc in docs_in_agent_output if doc not in docs_in_vectorstore]

    # Agent hallucinated files:
    if docs_hallucinated:
        content_overwrite = "I am sorry I could not find any information related to your question."
        return ModelResponse(
            result=[AIMessage(content=content_overwrite)],
            structured_response=ResponseFormat(response=content_overwrite, documents=[]),
        )

    # Correct response:
    return response
