from hack_zurich_app.agents.support_answer import SupportAnswer
from hack_zurich_app.rag.chain import policies_qa_chain


class PolicyInfoAgent:
    def __init__(self):
        print("Initializing PolicyInfoAgent...")
        self.qa_chain = policies_qa_chain()

    def ask(self, query: str) -> SupportAnswer:
        chain_output = self.qa_chain(query)
        answer = chain_output["result"]

        document_used = chain_output["source_documents"][0].metadata
        document_path = document_used['source']
        document_name = document_path.split("/")[-1]
        answer += f"\n\n See {document_name} page {document_used['page']}."

        return SupportAnswer(answer, document_path)
