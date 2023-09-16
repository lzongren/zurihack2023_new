import functools

from langchain import FAISS
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import VectorStore

from hack_zurich_app import data_catalog


def create_faiss_db(loader: BaseLoader) -> VectorStore:
    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)

    # Retrieve embedding function from code env resources
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    return db


@functools.lru_cache(maxsize=1)
def create_policies_db():
    loader = PyPDFDirectoryLoader(data_catalog.polices())

    return create_faiss_db(loader)


if __name__ == "__main__":
    query = "What is house hold insurance"
    docs = create_policies_db().similarity_search(query)

    for doc in docs:
        print(doc.page_content)
