from hack_zurich_app.agents.claim_agent import ClaimAgent
from hack_zurich_app.agents.policy_info_agent import PolicyInfoAgent
from hack_zurich_app.agents.routing_agent import RoutingAgent, QueryType
from hack_zurich_app.agents.support_answer import SupportAnswer


class SupportCenter:
    def __init__(self):
        print("Initializing SupportCenter...")
        self.routing_agent = RoutingAgent()
        self.policy_info_agent = PolicyInfoAgent()
        self.claim_agent = ClaimAgent()

    def ask(self, query: str) -> SupportAnswer:
        query_type = self.routing_agent.determine_query_type(query)
        if query_type == QueryType.POLICY_INFO:
            return self.policy_info_agent.ask(query)
        elif query_type == QueryType.CLAIM:
            return self.claim_agent.ask(query)
        else:
            assert False  # TODO


if __name__ == "__main__":
    support_center = SupportCenter()

    default_query = "What is house hold insurance?"

    while True:
        input_query = input(f"Enter the query [default:'{default_query}']") or default_query
        result = support_center.ask(input_query)
        print(result)
