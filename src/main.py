import uvicorn

from src.config.settings import settings


def start_api_server():
    """
    Start API Server
    :return:
    """
    uvicorn.run("src.server.api:app", port=settings.port, reload=True)


if __name__ == '__main__':
    start_api_server()
