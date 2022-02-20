import math

from Types import HouseholdType


class Waste:

    # Describes the coefficients of trash production for each household type compared to the base household production
    coeffRetired = 0.8
    coeffSingle = 1
    coeffCouple = 2
    coeffFamily = 2.5


    # The base trash production function using the formula given in the assignement
    @classmethod
    def produceTrash(cls, step, nbSteps):
        waste = 0
        if nbSteps > 0:
            for i in range(nbSteps):
                x = step+i
                waste += 40-0.04*x-math.exp(-0.01*x)*math.sin(0.3*x)
        return waste


    # Gives the household trash production depending on the type of the household
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


    # Gives the ammount of trash that the municipality will produce in the next 3 years (for renewing contracts)
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