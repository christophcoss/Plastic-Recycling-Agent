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
        return
    #TODO

    def seperateTrash(self):
        return
    #TODO

    def throwOutTrash(self):
        return
    #TODO

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