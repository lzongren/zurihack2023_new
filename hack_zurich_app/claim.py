def match_rules(claim, coverage_rules: list) -> list:
    pass


def determine_claim(claim: str, coverage_rules: list, exclusion_rules: list) -> bool:
    matched_coverage_rules = match_rules(claim, coverage_rules)
    matched_exclusion_rules = match_rules(claim, exclusion_rules)
    pass
