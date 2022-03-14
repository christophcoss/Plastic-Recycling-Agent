import math
import json

from Types import HouseholdType


class Waste:

    householdData = None

    @classmethod
    def init(cls, data):
        if cls.householdData is None:
            cls.householdData = data['households']



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
        wasteProd *= cls.householdData[type.value]['rateFactor']
        return wasteProd


    # Gives the ammount of trash that the municipality will produce in the next 3 years (for renewing contracts)
    #
    @classmethod
    def trashMunicipality(cls, step, nbSteps, population):
        wasteBase = cls.produceTrash(step,nbSteps)
        coeff = 0
        for pair in population:
            coeff += cls.householdData[pair[0].value]['rateFactor'] * pair[1]
        return wasteBase * coeff

    # def __init__(self, qPlastic, qNPlastic):
    #     self.qPlastic = qPlastic
    #     self.qNPlastic = qNPlastic
    #
    # def decreaseWaste(self):
    #     #TODO
    #     return