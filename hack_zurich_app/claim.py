from typing import Optional
from enum import Enum, auto
import logging
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from hack_zurich_app.rag import llm_provider


inclusion_rules = {
    'car insurance policy': {'applies to cars', 'applies to trucks'}
}
exclusion_rules = {
    'car insurance policy': {'applies to cars', 'applies to trucks'}
}
query = {
    ''
}


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


user_policies = {
   "userid1": set(["CGI housegold"])
}


class ClaimResult(Enum):
    COVERED = auto()
    NOT_COVERED = auto()
    INSUFFICIENT_CONTEXT = auto()
    POLICY_NOT_FOUND = auto()


class CoverageSpecialist():
    def __init__(self) -> None:
        logger.info("Creating coverage specialist instance")
        logger.info("Setting up coverage specialist LLM instance")
        self.llm = llm_provider.openai_llm()

    def determine_claim(self, user_id: str, claim: str) -> ClaimResult:
        # Determine policy in question
        policy_id: Optional[str] = self._get_policy_id(user_id, claim)
        
        if policy_id is None:
            return ClaimResult.POLICY_NOT_FOUND
        
        # get relevant rules
        coverage_rules, exclusion_rules = self._get_rules(policy_id)

        # Determine rules in scope
        coverage_rules_matching = {
            rule: self._match_coverage_rule(claim, rule)
            for rule in coverage_rules
        }
        matched_exclusion_rules = {
            rule: self._match_coverage_rule(claim, rule)
            for rule in coverage_rules
        }
        
        # If no coverage_rules_match then return NOT_COVERED
        #if all()

    def _get_policy_id(self, user_id: str, claim: str) -> Optional[str]:
        return "policyA"

    def _get_rules(self, policy_id) -> tuple[list, list]:
        # use knowledge base
        return coverage_rules, exclusion_rules

    def _match_coverage_rule(self, claim: str, rule: str) -> Optional[bool]:
        prompt_text = """
        You analyze insurance claim against a policy coverage rule.
        You answer the question "Does the RULE cover the CLAIM?".
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
        prompt = f"""
        You analyze insurance claim against a policy coverage exclusion rule.
        You answer the question "Does the exclusion RULE exclude cover for the CLAIM?".
        You answer only with YES, NO, INSUFFICIENT_CONTEXT.
        RULE: {rule}
        CLAIM: {claim}
        """
        logger.info(f"Matching claim against coverage rule: {rule}")
        result = self.llm.generate
        if 'YES' in result:
            return True
        elif 'NO' in result:
            return False
        return None


def main():
    logger.info("Initializing coverage specialist")
    specialist = CoverageSpecialist()
    


if __name__ == '__main__':
    main()