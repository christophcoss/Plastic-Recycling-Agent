import math

from Types import HouseholdType


class Waste:
    coeffRetired = 0.7
    coeffSingle = 1
    coeffCouple = 1.7
    coeffFamily = 3

    @classmethod
    def produceTrash(cls, step, nbSteps):
        waste = 0
        if nbSteps > 0:
            for i in range(nbSteps):
                x = step+i
                waste += 40-0.04*x-math.exp(-0.01*x)*math.sin(0.3*x)
        return waste


    @classmethod
    def trashHousehold(cls, step, type):
        wasteProd = cls.produceTrash(step,1)
        if type == HouseholdType.RETIRED:
            wasteProd *= cls.coeffRetired
        elif type == HouseholdType.SINGLE:
            wasteProd *= cls.coeffSingle
        elif type == HouseholdType.COUPLE:
            wasteProd *= cls.coeffCouple
        else:
            wasteProd *= cls.coeffFamily
        return wasteProd


    @classmethod
    def trashMunicipality(cls, step, nbSteps, population):
        wasteBase = cls.produceTrash(step,nbSteps)
        coeff = 0
        for pair in population:
            if pair[0] == HouseholdType.RETIRED:
                coeff += cls.coeffRetired * pair[1]
            elif pair[0] == HouseholdType.SINGLE:
                coeff += cls.coeffSingle * pair[1]
            elif pair[0] == HouseholdType.COUPLE:
                coeff += cls.coeffCouple * pair[1]
            elif pair[0] == HouseholdType.FAMILY:
                coeff += cls.coeffFamily * pair[1]
        return wasteBase * coeff

    # def __init__(self, qPlastic, qNPlastic):
    #     self.qPlastic = qPlastic
    #     self.qNPlastic = qNPlastic
    #
    # def decreaseWaste(self):
    #     #TODO
    #     return