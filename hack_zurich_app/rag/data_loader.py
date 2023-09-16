import functools
import logging

from langchain import FAISS
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import VectorStore

from hack_zurich_app import data_catalog

logger = logging.getLogger(__file__)


def create_docs_chunks(loader: BaseLoader) -> VectorStore:
    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)

    return chunks


def create_faiss_db(loader: BaseLoader) -> VectorStore:
    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)

    # Retrieve embedding function from code env resources
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    return db


@functools.lru_cache(maxsize=1)
def create_policies_db():
    logger.info("Initializing policies vectors db...")
    loader = PyPDFDirectoryLoader(data_catalog.polices())

    return create_faiss_db(loader)


@functools.lru_cache(maxsize=1)
def get_policies_docs():
    logger.info("Initializing policies vectors db...")
    loader = PyPDFDirectoryLoader(data_catalog.polices())

    return create_docs_chunks(loader)


if __name__ == "__main__":
    policies_db = create_policies_db()

    default_query = "What is house hold insurance?"

    while True:
        query = input(f"Enter the query [default:'{default_query}']") or default_query

        docs = policies_db.similarity_search(query)
        for doc in docs:
            print("\n=== Doc ===")
            print(doc.page_content)
