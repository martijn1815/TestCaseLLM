import uuid
from datetime import datetime
from fastapi import FastAPI, Body
from typing import Annotated
from pydantic import BaseModel, Field

from src.llm_agent.config.logger import logger


class Input(BaseModel):
    prompt: str


class Output(BaseModel):
    id: str
    response: str
    created_at: str | None = Field(default=str(datetime.now()))

app = FastAPI()


@app.post("/responses/", response_model=Output)
async def receive_prompt(input: Annotated[Input, Body(examples=[{"prompt": "Hello World"}])]):
    logger.info(f"'input': {input.model_dump()}")
    output = Output(
        id=str(uuid.uuid1()),
        response='Hello World'
    )
    logger.info(f"'output': {output.model_dump()}")
    return output
