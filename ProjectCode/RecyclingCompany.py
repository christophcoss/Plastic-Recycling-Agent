from mesa import Agent
from enum import *

class RecyclingCompany(Agent):
    def __init__(self, unique_id, model, technology, offers, recyclingRate):
        super().__init__(unique_id, model)
        self.technology = technology
        self.offers = offers
        self.recyclingRate = recyclingRate

    def submitOffers(self):
        return
    #TODO

class Technology(Enum):
    FILTRATION = "Filtration"
    NIR = "NIR"
    FLAKING = "Falking"
    WASHING = "Washing"
    GRANULATING = "Granulating"
    COMPOUNDING = "Compounding"
