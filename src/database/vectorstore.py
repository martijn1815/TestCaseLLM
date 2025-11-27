import os
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings

from src.config.settings import settings


embedding_model = OllamaEmbeddings(
    model=settings.embedding_model,
    base_url=settings.embedding_host_url,
)

vector_store = InMemoryVectorStore(embedding=embedding_model)

def load_markdown_files(directory: str):
    """
    Loads markdown/text files from given directory and returns a list of documents.
    :param directory:
    :return documents:
    """
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                loader = TextLoader(path)
                docs = loader.load()

                # Add filename as metadata
                for d in docs:
                    d.metadata["file_name"] = file
                    documents.append(d)

    return documents


def ingest_md_files():
    """
    Load and ingest Markdown files into the vector store. This function should run on start up.
    Improvements for a productions environment should include a check which documents have already been ingested.
    """
    docs = load_markdown_files(settings.file_dir)
    vector_store.add_documents(
        documents=docs
    )
