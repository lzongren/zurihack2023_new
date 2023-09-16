import unittest
from hack_zurich_app.claim import CoverageSpecialist


class TestClaim(unittest.TestCase):
    def test_insufficient_information(self):
        specialist = CoverageSpecialist()
        user_id = "1"
        claim = """Am I covered for damage to my car by a friend"""
        specialist.determine_claim(user_id, claim)
        result = False
        target = True
        self.assertEqual(result, target)

    def test_match_coverage_rule_no(self):
        specialist = CoverageSpecialist()
        result = specialist._match_coverage_rule(rule="Dogs are not insured", claim="Is my car ensured?")
        target = False
        self.assertEqual(result, target)

    def test_match_coverage_rule_insufficient(self):
        specialist = CoverageSpecialist()
        result = specialist._match_coverage_rule(rule="Some cars are insured", claim="Is my car ensured?")
        self.assertIsNone(result)

    def test_match_coverage_rule_yes(self):
        specialist = CoverageSpecialist()
        result = specialist._match_coverage_rule(rule="Cars are insured", claim="Is my car ensured?")
        target = True
        self.assertEqual(result, target)

    def test_match_coverage_exclusion_rule_no(self):
        specialist = CoverageSpecialist()
        result = specialist._match_exclusion_rule(
            rule="10 years old cars or older are not insured in case of accidents",
            claim="Is my 5 years old car insured?"
        )
        target = False
        self.assertEqual(result, target)

    def test_match_coverage_exclusion_rule_insufficient(self):
        specialist = CoverageSpecialist()
        result = specialist._match_exclusion_rule(
            rule="10 years old cars or older are not insured in case of accidents",
            claim="Is my car insured?"
        )
        self.assertIsNone(result)

    def test_match_coverage_eclusion_rule_yes(self):
        specialist = CoverageSpecialist()
        result = specialist._match_exclusion_rule(
            rule="The insurance does not cover damage due to lack of oil.",
            claim="My car had no oil and engine got damaged. Is this covered?"
        )
        target = True
        self.assertEqual(result, target)


if __name__ == '__main__':
    unittest.main()