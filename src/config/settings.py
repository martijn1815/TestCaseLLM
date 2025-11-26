from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    # API
    api_port: int
    log_file: str | None = "../logfiles/policy_agent.log"
    # LLM Model
    host_url: str | None = None
    model: str
    host_url: str
    # Embedding Model
    embedding_model: str
    embedding_host_url: str | None = None
    file_dir: str  | None = "../../test_data/synthetic_policy_documents/"

    class Config:
        env_file = ".env"


settings = Settings()
