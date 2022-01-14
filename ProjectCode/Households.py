from mesa import Agent
from enum import *
from Waste import Waste

class Households(Agent):
    def __init__(self, unique_id, model, type, infraAccess, recPerception, recImportance, recKnowledge, connected, proDecRate, recPlaCons, wasteProd):
        super().__init__(unique_id, model)
        self.type = type #defines the ammount of trash produced
        self.infraAccess = infraAccess #how difficult it is for them to recycle
        self.recPerception = recPerception #how perceptive they are to changing their importance of recycling
        self.recImportance = recImportance #how important it is for them to recycle
        self.recKnowledge = recKnowledge #how good they are at recycling
        self.connected = connected
        self.prodDecRate = proDecRate
        self.recPlaCons = recPlaCons
        self.wasteProd = wasteProd

    def produceTrash(self):
        if self.type == HouseholdType.INDIVIDUALS:
            self.wasteProd == 9.5
        if self.type == HouseholdType.COUPLES:
            self.wasteProd == 19
        if self.type == HouseholdType.FAMILIES:
            self.wasteProd == 23.5
        if self.type == HouseholdType.RETIRED:
            self.wasteProd == 7.5


    #Unsure about this
    def seperateTrash(self):
        plastics = self.wasteProd * 0.195
        qPlastic = plastics * self.recImportance * self.recKnowledge
        qNPlastic = plastics * (1-self.recKnowledge * self.recImportance)
        return Waste(qPlastic, qNPlastic)

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

class HouseholdType(Enum):
    INDIVIDUALS = "Individuals"
    COUPLES = "Couples"
    FAMILIES = "Families"
    RETIRED = "Retired"