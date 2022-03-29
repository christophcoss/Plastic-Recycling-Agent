from enum import *

class HouseholdType(Enum):
    RETIRED = "retired"
    SINGLE  = "single"
    COUPLE  = "couple"
    FAMILY  = "family"

    @classmethod
    def get_index(cls, type):
        return list(cls).index(type)

class CollectionType(Enum):
    AT_HOME = "At home"
    CENTRALIZED = "Centralized"

class Technology(Enum):
    FILTRATION = "Filtration"
    NIR = "NIR"
    FLAKING = "Falking"
    WASHING = "Washing"
    GRANULATING = "Granulating"
    COMPOUNDING = "Compounding"



