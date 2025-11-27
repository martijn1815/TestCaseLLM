
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from src.config.logger import logger
from src.database.vectorstore import ingest_md_files
from src.server.models import Prompt, Output, Feedback
from src.agent.agent import get_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start ingesting files into vectorstore")
    ingest_md_files()
    logger.info("Finished ingesting files into vectorstore")
    logger.info("Starting API Server")
    yield
    logger.info("Shutting down API Server")


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.info(f"'exception_handler': {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.post("/prompt/", response_model=Output)
async def receive_prompt(
        prompt: Annotated[
            Prompt,
            Body(examples=[{
                "prompt": "Hello World",
                "conversation_id": "Optional conversation id"
            }])
        ]
    ):
    logger.info(f"{{'prompt': {prompt.model_dump()}}}")
    agent_response = get_response(thread_id=prompt.conversation_id, prompt=prompt.prompt)
    output = Output(
        conversation_id=prompt.conversation_id,
        response=agent_response.response,
        documents=agent_response.documents
    )
    logger.info(f"{{'output': {output.model_dump()}}}")
    return output


@app.post("/feedback/")
async def receive_prompt(feedback: Feedback):
    logger.info(f"{{'feedback': {feedback.model_dump()}}}")
