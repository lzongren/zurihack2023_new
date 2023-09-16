import os

from langchain import OpenAI
from langchain.chains import RetrievalQA

from hack_zurich_app.rag import data_loader

os.environ["OPENAI_API_KEY"] = "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"

llm = OpenAI()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=data_loader.db.as_retriever(),
)

if __name__ == "__main__":

    while True:
        query = input()
        result = qa.run(query)
        print(result)