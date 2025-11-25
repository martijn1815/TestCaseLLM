import uvicorn

from src.llm_agent.config.settings import settings


if __name__ == '__main__':
    uvicorn.run("src.llm_agent.server.api:app", port=settings.port, reload=True)