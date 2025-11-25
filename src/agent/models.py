from pydantic import BaseModel


class ResponseFormat(BaseModel):
    """ Response schema for the agent. """
    response: str
