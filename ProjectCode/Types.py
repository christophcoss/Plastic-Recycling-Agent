from enum import *

class HouseholdType(Enum):
    RETIRED = "Retired"
    SINGLE  = "Individuals"
    COUPLE  = "Couple"
    FAMILY  = "Family"


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



