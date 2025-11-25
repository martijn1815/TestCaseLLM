import uvicorn

from src.llm_agent.config.settings import settings
from src.llm_agent.config.logger import logger


def start_api_server():
    """
    Start API Server
    :return:
    """
    logger.info("Starting API Server")
    uvicorn.run("src.llm_agent.server.api:app", port=settings.port, reload=True)


if __name__ == '__main__':
    start_api_server()
