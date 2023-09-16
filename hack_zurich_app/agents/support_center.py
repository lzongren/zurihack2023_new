from hack_zurich_app.agents.coverage_agent import CoverageAgent
from hack_zurich_app.agents.policy_info_agent import PolicyInfoAgent
from hack_zurich_app.agents.routing_agent import RoutingAgent, QueryType
from hack_zurich_app.agents.support_answer import SupportAnswer


class SupportCenter:
    def __init__(self):
        print("Initializing SupportCenter...")
        self.routing_agent = RoutingAgent()
        self.policy_info_agent = PolicyInfoAgent()
        self.coverage_agent = CoverageAgent()

    def ask(self, query: str) -> SupportAnswer:
        query_type = self.routing_agent.determine_query_type(query)

        if query_type == QueryType.POLICY_INFO:
            return self.policy_info_agent.ask(query)
        elif query_type == QueryType.COVERAGE:
            return self.coverage_agent.ask(query)
        else:
            return SupportAnswer("This type of query is not supported yet", None)


if __name__ == "__main__":
    support_center = SupportCenter()

    default_query = "What is house hold insurance?"

    while True:
        input_query = input(f"Enter the query [default:'{default_query}']") or default_query
        result = support_center.ask(input_query)
        print(result)
