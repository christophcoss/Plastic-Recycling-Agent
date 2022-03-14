# Activities are actions taken by the municipality to increase the total recycling procifiency of its households.

class Activity:
    def __init__(self, activity):
        self.name = activity["Name"]
        self.attribute = activity["Attribute"]
        self.cost = activity["Cost"]
        self.efficiency = activity["Efficiency"]
        self.scaledCost = activity["ScaledCost"]
        self.stepsToEffect = activity["StepsToEffect"]
        self.effectOnStep = 0

    def totalCost(self, nbHouseholds):
        if self.scaledCost :
            return nbHouseholds * self.cost
        else :
            return self.cost

    def relativeEfficiency(self, population, nbHouseholds):
        efficiency = 0
        for pop in population:
            efficiency += self.efficiency[pop[0].value] * pop[1]
        return 0 if nbHouseholds == 0 else abs(efficiency / nbHouseholds)
