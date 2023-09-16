from enum import auto, Enum


class QueryType(Enum):
    CLAIM = auto()
    POLICY_INFO = auto()


class RoutingAgent:
    def __init__(self):
        print("Initializing ClaimAgent...")
        # TODO

    def determine_query_type(self, query) -> QueryType:
        # TODO
        return QueryType.POLICY_INFO
