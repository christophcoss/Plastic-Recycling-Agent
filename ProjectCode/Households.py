from mesa import Agent
from enum import *

class Households(Agent):
    def __init__(self, unique_id, model, type, infraAccess, recPerception, recImportance, recKnowledge, connected, proDecRate, recPlaCons, wasteProd):
        super().__init__(unique_id, model)
        self.type = type
        self.infraAccess = infraAccess
        self.recPreception = recPerception
        self.recImportance = recImportance
        self.recKnowledge = recKnowledge
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




class HouseholdType(Enum):
    INDIVIDUALS = "Individuals"
    COUPLES = "Couples"
    FAMILIES = "Families"
    RETIRED = "Retired"