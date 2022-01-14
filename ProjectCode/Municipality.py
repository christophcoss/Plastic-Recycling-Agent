from mesa import Agent
from Activity import Activity

class Municipality(Agent):
    def __init__(self, unique_id, model, recTarget, recBudget, activityList):
        super().__init__(unique_id, model)
        self.recTarget = recTarget
        self.recBudget = recBudget
        self.activityList = activityList

    def chooseOffer(self, listOffers):
        return
    #TODO

    def collectFines(self, fineAmount):
        return
    #TODO

    def setCollectionRate(self, rate):
        return
    #TODO

    def makeActivities(self):
        return
