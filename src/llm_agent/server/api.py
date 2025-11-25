import uuid
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Body, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.llm_agent.config.logger import logger


class Input(BaseModel):
    id: SkipJsonSchema[str] | None = Field(default=str(uuid.uuid1()))
    created_at: SkipJsonSchema[str] | None = Field(default=str(datetime.now()))
    prompt: str


class Output(BaseModel):
    id: str | None = Field(default=str(uuid.uuid1()))
    created_at: str | None = Field(default=str(datetime.now()))
    response: str

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(exc.errors())
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.post("/responses/", response_model=Output)
async def receive_prompt(input: Annotated[Input, Body(examples=[{"prompt": "Hello World"}])]):
    logger.info(f"'input': {input.model_dump()}")
    output = Output(
        response='Hello World'
    )
    logger.info(f"'output': {output.model_dump()}")
    return output
