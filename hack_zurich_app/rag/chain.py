import functools

from langchain.chains import RetrievalQA

from hack_zurich_app.rag import data_loader, llm_provider


def retrieval_qa_chain(llm, vector_db):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(),
    )

    return qa


@functools.lru_cache(maxsize=1)
def policies_qa_chain():
    llm = llm_provider.openai_llm()
    vector_db = data_loader.create_policies_db()

    return retrieval_qa_chain(llm, vector_db)


if __name__ == "__main__":
    print("Initializing policies QA chain...")
    qa_chain = policies_qa_chain()

    default_query = "What is house hold insurance?"

    while True:
        query = input(f"Enter the query [default:'{default_query}']") or default_query
        result = qa_chain.run(query)
        print(result)
