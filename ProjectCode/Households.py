import math

from mesa import Agent
from enum import *
from Waste import Waste


class Households(Agent):
    def __init__(self, unique_id, model, municipality, type, infraAccess, recPerception, recImportance, recKnowledge):
        super().__init__(unique_id, model)
        self.municipality = municipality
        self.type = type #defines the ammount of trash produced
        self.infraAccess = infraAccess #how difficult it is for them to recycle
        self.recPerception = recPerception #how perceptive they are to changing their importance of recycling
        self.recImportance = recImportance #how important it is for them to recycle
        self.recKnowledge = recKnowledge #how good they are at recycling
        self.wasteProd = 0
        self.wastePlastic = 0
        self.wasteNPlastic = 0
        self.wastePlasticDispo = 0
        self.wasteNPlasticDispo = 0


    def produceTrash(self):
        x = self.model.schedule.steps
        wasteProd = 40-0.04*x-math.exp(-0.01*x)*math.sin(0.3*x)
        if self.type == HouseholdType.RETIRED:
            # self.wasteProd == 7.5
            wasteProd *= 0.7
        elif self.type == HouseholdType.SINGLE:
            # self.wasteProd == 9.5
            pass
        elif self.type == HouseholdType.COUPLES:
            # self.wasteProd == 19
            wasteProd *= 1.2
        else:
            # self.wasteProd == 23.5
            wasteProd *= 2

        plastic = self.separateTrash(wasteProd)
        self.wasteProd += wasteProd
        self.wastePlastic += plastic
        self.wasteNPlastic += (wasteProd-plastic)
        self.wastePlasticDispo += plastic
        self.wasteNPlasticDispo += (wasteProd-plastic)


    #Unsure about this
    def separateTrash(self, wasteProd):
        if not self.infraAccess:
            return 0
        plastics = wasteProd * 0.195
        return plastics * self.recImportance * self.recKnowledge


    def throwOutTrash(self):
        return
    #TODO

    # add perception
    def improveImportance(self, Activity):
        if not self.connected:
            return
        newRecImp = (self.recImportance * (1 + Activity.efficiency))
        self.recImportance = newRecImp if newRecImp < 1 else 1


    def improveKnowledge(self, Activity):
        if not self.connected:
            return
        newRecKnow = (self.recKnowledge * (1 + Activity.efficiency))
        self.recImportance = newRecKnow if newRecKnow < 1 else 1


    def step(self):
        self.produceTrash()



class HouseholdType(Enum):
    INDIVIDUALS = "Individuals"
    COUPLES = "Couples"
    FAMILIES = "Families"
    RETIRED = "Retired"