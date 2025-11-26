from pydantic import BaseModel, Field

from src.agent.prompts import DOCUMENTS_FIELD_PROMPT


class ResponseFormat(BaseModel):
    """ Response schema for the agent. """
    response: str
    documents: list[str] = Field(description=DOCUMENTS_FIELD_PROMPT)
