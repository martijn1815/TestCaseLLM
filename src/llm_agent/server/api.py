import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field


class Input(BaseModel):
    prompt: str


class Output(BaseModel):
    id: str
    response: str
    created_at: datetime | None = Field(default=datetime.now())

app = FastAPI()


@app.post("/responses/", response_model=Output)
async def create_item(item: Input):
    return Output(
        id=str(uuid.uuid1()),
        response='Hello World'
    )
