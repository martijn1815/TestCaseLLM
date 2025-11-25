import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema


class Prompt(BaseModel):
    """ Prompt input schema for API Post request """
    id: SkipJsonSchema[str] | None = Field(default=str(uuid.uuid1()))
    created_at: SkipJsonSchema[str] | None = Field(default=str(datetime.now()))
    prompt: str


class Output(BaseModel):
    """ Prompt output schema for API Post request """
    id: str | None = Field(default=str(uuid.uuid1()))
    created_at: str | None = Field(default=str(datetime.now()))
    response: str
