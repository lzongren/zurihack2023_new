from hack_zurich_app.agents.support_answer import SupportAnswer
from typing import Optional
from enum import Enum, auto
import logging
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from hack_zurich_app.rag import llm_provider


class ClaimResult(Enum):
    COVERED = auto()
    NOT_COVERED = auto()
    EXCLUDED = auto()
    INSUFFICIENT_CONTEXT = auto()
    POLICY_NOT_FOUND = auto()


inclusion_rules = {
    'accidental damage insurance': {
        'The insurance covers damage caused against the policy holders will to the declared vehicle',
        'The insurance covers the damage caused by collisions between the declared vehicle and animals',
        'Damage caused by evasive maneuvers does not constitute damage caused by animals',
        'Vandalism: The insurance covers the puncturing of the tires by vandals.'
    }
}
exclusion_rules = {
    'accidental damage insurance': {
        'Exclusions: the insurance does not cover damage due to vehicle operation: due to lack of oil',
        'Exclusions: the insurance does not cover damage due to vehicle due to vehicle operation, wear and tear',
        'Exclusions: the insurance does not cover damage due to operation of vehicle due to illegal driving',
        'The insurance does not cover accessories that can also be used independently of the vehicle'
    }
}

response_mapping = {
    ClaimResult.COVERED: "The answer should explain that the claim is covered by the policy",
    ClaimResult.INSUFFICIENT_CONTEXT: "The answer should explain that more context should be provided to determine weather the claim should be covered",
    ClaimResult.EXCLUDED: "The claim in question is excluded from the policy",
    ClaimResult.POLICY_NOT_FOUND: "The policy in question does not exist or is not known",
    ClaimResult.NOT_COVERED: "The policy in question does not cover the claim",
}


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


user_policies = {
   "userid1": set(["CGI housegold"])
}


class CoverageAgent():
    def __init__(self) -> None:
        logger.info("Creating coverage specialist instance")
        logger.info("Setting up coverage specialist LLM instance")
        self.llm = llm_provider.openai_llm()

    def ask(self, query: str) -> SupportAnswer:
        # TODO provide it with context
        user_id: str = 1
        # Determine policy in question
        policy_id: Optional[str] = self._get_policy_id(user_id, query)
        
        if policy_id is None:
            decision = ClaimResult.POLICY_NOT_FOUND
        else:
            decision = ClaimResult.NOT_COVERED
            # get relevant rules
            coverage_rules, exclusion_rules = self._get_rules(policy_id)

            # Determine rules in scope
            coverage_rules_matching = {
                rule: self._match_coverage_rule(query, rule)
                for rule in coverage_rules
            }
            matched_exclusion_rules = {
                rule: self._match_exclusion_rule(query, rule)
                for rule in exclusion_rules
            }

            # If no coverage_rules_match then return NOT_COVERED
            if True not in coverage_rules_matching.values():
                decision = ClaimResult.NOT_COVERED
            elif all(match is False for rule, match in matched_exclusion_rules.items()):
                decision = ClaimResult.COVERED
            elif any(match is True for rule, match in matched_exclusion_rules.items()):
                decision = ClaimResult.EXCLUDED
            else:
                decision = ClaimResult.INSUFFICIENT_CONTEXT
        reply = self._reply_to_claim(query, decision)
        return SupportAnswer(reply, None)

    def _get_policy_id(self, user_id: str, claim: str) -> Optional[str]:
        return "accidental damage insurance"

    def _get_rules(self, policy_id) -> tuple[list, list]:
        # use knowledge base
        return inclusion_rules[policy_id], exclusion_rules[policy_id]

    def _match_coverage_rule(self, claim: str, rule: str) -> Optional[bool]:
        prompt_text = """
        You analyze insurance claim against a policy coverage rule.
        You answer the question "Does the RULE cover the CLAIM?".
        We want to reduce false positives.
        You answer only with YES, NO, INSUFFICIENT_CONTEXT.
        RULE: {rule}
        CLAIM: {claim}
        """
        
        # Step 4: Define the Prompt Template
        prompt = PromptTemplate(
            input_variables=["rule", "claim"],
            template=prompt_text,
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        logger.info(f"Matching claim against coverage rule: {rule}")
        result = chain.run(rule=rule, claim=claim).strip()
        
        if 'NO' in result:
            return False
        elif 'YES' in result:
            return True
        else:
            return None
  
    def _match_exclusion_rule(self, claim: str, rule: str) -> Optional[bool]:
        # TODO generate prompt and parse the result
        prompt_text = """
        You answer the question "Is there a reason to reject the CLAIM given the EXCLUSION RULE?".
        You answer only with THERE_IS, THERE_ISNT, INSUFFICIENT_CONTEXT.
        You want to say THERE_ISNT if the CLAIM is rejected because of the EXCLUSION RULE.
        EXCLUSION RULE: '{rule}'
        CLAIM: '{claim}'
        """
        # Step 4: Define the Prompt Template
        prompt = PromptTemplate(
            input_variables=["rule", "claim"],
            template=prompt_text,
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        logger.info(f"Matching claim against coverage exclusion rule: {rule}")
        result = chain.run(rule=rule, claim=claim).strip()
        
        if 'THERE_ISNT' in result:
            return False
        elif 'THERE_IS' in result:
            return True
        else:
            return None

    def _reply_to_claim(self, claim: str, decision: ClaimResult) -> str:
        prompt_text = """
        Write an answer to the CLAIM coming from a user. Don't start it with "Answer:".
        {status}
        CLAIM: '{claim}'
        """
        # Step 4: Define the Prompt Template
        prompt = PromptTemplate(
            input_variables=["claim", "status"],
            template=prompt_text,
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        logger.info(f"Replying to the following decision: {decision}")
        result = chain.run(
            status=response_mapping[decision],
            claim=claim
        )
        
        return result


def main():
    logger.info("Initializing coverage specialist")
    specialist = CoverageAgent()


if __name__ == '__main__':
    main()
