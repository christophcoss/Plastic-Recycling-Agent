# Activities are actions taken by the municipality to increase the total recycling procifiency of its households.

class Activity:
    def __init__(self, activity):
        self.name = activity["Name"]
        self.attribute = activity["Attribute"]
        self.cost = activity["Cost"]
        self.efficiency = activity["Efficiency"]
        self.ScaledCost = activity["ScaledCost"]

    def totalCost(self, nbHouseholds):
        if self.ScaledCost :
            return nbHouseholds * self.cost
        else :
            return self.cost
