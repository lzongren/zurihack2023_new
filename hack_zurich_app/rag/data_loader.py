from langchain import FAISS
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from hack_zurich_app import file_utils

# Load the PDF file and split it into smaller chunks

loader = PyPDFDirectoryLoader(file_utils.data_dir())
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
docs = loader.load()
chunks = text_splitter.split_documents(docs)

# Retrieve embedding function from code env resources
embeddings = HuggingFaceEmbeddings()
db = FAISS.from_documents(docs, embeddings)

if __name__ == "__main__":
    query = "What did the president say about Ketanji Brown Jackson"
    docs = db.similarity_search(query)
    print(docs[0].page_content)