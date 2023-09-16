from hack_zurich_app.rag.chain import policies_qa_chain


class PolicyInfoAgent:
    def __init__(self):
        print("Initializing PolicyInfoAgent...")
        self.qa_chain = policies_qa_chain()

    def ask(self, query: str):
        return self.qa_chain(query)
