import typing

from pydantic import BaseModel


class Cause(BaseModel):
    description: str


class Benefit(BaseModel):
    description: str


class Subject(BaseModel):
    description: str


class Damage(BaseModel):
    description: str
    # caused_by
    causes: typing.List[Cause] = list()
    # compensated_by
    benefits: typing.List[Benefit] = list()
    # damage_on
    subjects: typing.List[Subject] = list()

    def __str__(self):
        subject = " or ".join([s.description for s in self.subjects])
        cause = " or ".join([c.description for c in self.causes])
        benefit_desc = " or ".join([b.description for b in self.benefits])
        return f"{self.description} caused by {cause} on {subject} is compensated by {benefit_desc}"


class SpecificInsurance(BaseModel):
    covers: typing.List[Damage] = list()
    excludes: typing.List[Damage] = list()


class GeneralInsurancePolicies(BaseModel):
    specific_insurances: typing.List[SpecificInsurance]


if __name__ == "__main__":
    motor_vehicle_gci = GeneralInsurancePolicies(
        specific_insurances=[
            SpecificInsurance(
                covers=[
                    Damage(
                        description="death or bodily injury",
                        causes=[
                            Cause(
                                description="traffic accident when vehicle not in action"
                            ),
                            Cause(description="vehicle operation of action"),
                        ],
                        benfits=[Benefit(description="limited to 100 mi CHF")],
                        subjects=[Subject(description="insured person")],
                    ),
                    Damage(
                        description="death or injury",
                        causes=[
                            Cause(
                                description="traffic accident when vehicle not in action"
                            ),
                            Cause(description="vehicle operation of action"),
                        ],
                        benfits=[Benefit(description="limited to 5 mi CHF")],
                        subjects=[
                            Subject(description="animal"),
                            Subject(description="property"),
                        ],
                    ),
                ]
            )
        ]
    )

    for spec_insur in motor_vehicle_gci.specific_insurances:
        for coverage in spec_insur.covers:
            print(coverage)

        for exclusion in spec_insur.excludes:
            print(exclusion)
