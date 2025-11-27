import uuid
from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from pydantic.json_schema import SkipJsonSchema


class Prompt(BaseModel):
    """ Prompt input schema for API Post request """
    message_id: SkipJsonSchema[str] | None = Field(default=str(uuid.uuid1()))
    conversation_id: str | None = Field(default=str(uuid.uuid1()))
    created_at: SkipJsonSchema[str] | None = Field(default=str(datetime.now()))
    prompt: str


class Output(BaseModel):
    """ Prompt output schema for API Post request """
    message_id: str | None = Field(default=str(uuid.uuid1()))
    conversation_id: str | None = Field(default=str(uuid.uuid1()))
    created_at: str | None = Field(default=str(datetime.now()))
    response: str
    documents: list[str] | None = []


class Feedback(BaseModel):
    """ Agent feedback schema for API Post request """
    feedback_id: SkipJsonSchema[str] | None = Field(default=str(uuid.uuid1()))
    conversation_id: str
    created_at: SkipJsonSchema[str] | None = Field(default=str(datetime.now()))
    feedback: str | None = None
    thumbs_up: bool | None = False
    thumbs_down: bool | None = False

    @model_validator(mode="after")
    def validate_thumbs(cls, values):
        if values.thumbs_up and values.thumbs_down:
            raise ValueError("Only one of thumbs_up or thumbs_down may be True.")
        return values
