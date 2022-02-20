import math

from mesa import Agent

# from enum import *
from Waste import *
# from Types import HouseholdType
from Types import CollectionType


# Households are the main agent of the model.
# - They belong to a municipality
# - They are one of these types: [Retired, Single, Couple, Family]
# - They have (or don't) access to the main recycling grid infrastructure (making recycling possible)
# - They have (or not) collection of waste directly from their household
# - They have a distance to centralized recycling system)
# - They have perception importance and knowledge of recycling


class Household(Agent):
    def __init__(self, unique_id, model, municipality, type, infraAccess, collectAtHome, distance, recPerception, recImportance, recKnowledge):
        super().__init__(unique_id, model)
        self.municipality = municipality
        self.type = type
        self.infraAccess = infraAccess
        self.collectAtHome = collectAtHome #f at home collection is avail;able for this household
        self.distanceFromCentralizedSystem = distance
        self.recPerception = recPerception #how perceptive they are to changing their importance of recycling
        self.recImportance = recImportance #how important it is for them to recycle
        self.recKnowledge = recKnowledge #how good they are at recycling
        self.wasteProd = 0
        self.wastePlastic = 0
        self.wasteNPlastic = 0
        self.wastePlasticToThrow = 0
        self.wasteNPlasticToThrow = 0

    # To Modify this is not good
    def improveImportance(self, Activity):
        newRecImp = self.recImportance * (1 + Activity.efficiency)
        self.recImportance = min(newRecImp, 1)

    # To Modify this is not good
    def improvePerception(self, Activity):
        newRecPer = self.recPerception * (1 + Activity.efficiency)
        self.recPerception = min(newRecPer, 1)

    # To Modify this is not good
    def improveKnowledge(self, Activity):
        newRecKnow = (self.recKnowledge * (1 + Activity.efficiency))
        self.recImportance = min(newRecKnow, 1)


    def produceAndSortTrash(self, step):
        wasteProd = Waste.trashHousehold(step, self.type)

        plastic = self.separateTrash(wasteProd)
        self.wasteProd += wasteProd
        self.wastePlastic += plastic
        self.wasteNPlastic += (wasteProd-plastic)
        self.wastePlasticToThrow += plastic
        self.wasteNPlasticToThrow += (wasteProd-plastic)


    #Unsure about this
    def separateTrash(self, wasteProd):
        if not self.infraAccess:
            return 0
        plastics = wasteProd * 0.195
        return plastics * self.recImportance * self.recKnowledge


    def step(self):
        step = self.model.schedule.steps
        self.produceAndSortTrash(step)
        self.throwOutTrash(step)


    # if centralized collection is available and not too far away then it is the choosen option
    # otherwise collection at home is choosen if available
    def throwOutTrash(self, step):
        contracts = [a for a in self.municipality.contracts \
                     if a.start <= step and step < a.end and \
                        (self.collectAtHome or a.type == CollectionType.CENTRALIZED) and \
                        a.full == False]
        if (len(contracts) > 1):
            if self.distanceFromCentralizedSystem < 50 :
                contracts.sort(key = lambda x: x.type.value, reverse = True)
            else:
                contracts.sort(key = lambda x: x.type.value)
        for contract in contracts :
            avail = contract.baseWaste - contract.collectedWaste
            wasteToThrow = self.wastePlasticToThrow + self.wasteNPlasticToThrow
            if  avail >= wasteToThrow:
                contract.collectedWaste += self.wastePlasticToThrow + self.wasteNPlasticToThrow
                contract.collectedPlastic += self.wastePlasticToThrow
                self.wastePlasticToThrow = 0
                self.wasteNPlasticToThrow = 0
            else:
                contract.full = True
                plastic = self.wastePlasticToThrow * avail /wasteToThrow
                nonPlastic = self.wasteNPlasticToThrow * avail /wasteToThrow
                contract.collectedWaste += avail
                contract.collectedPlastic += plastic
                self.wastePlasticToThrow  -= plastic
                self.wasteNPlasticToThrow -= nonPlastic
        return



