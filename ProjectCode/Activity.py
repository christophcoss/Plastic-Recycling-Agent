# Activities are actions taken by the municipality to increase the total recycling procifiency of its households.

class Activity:
    def __init__(self, activity):
        self.name = activity["Name"]
        self.attribute = activity["Attribute"]
        self.cost = activity["Cost"]
        self.efficiency = activity["Efficiency"]
        self.scaledCost = activity["ScaledCost"]
        self.stepsToEffect = activity["StepsToEffect"]

    def totalCost(self, nbHouseholds):
        if self.scaledCost :
            return nbHouseholds * self.cost
        else :
            return self.cost
