import random
from mesa import Agent

from Offer import Offer
from Util import *
# from Types import Technology

# Recycling Company is an agent in the model. There are several of them for each municipality.
class RecyclingCompany(Agent):
    def __init__(self, unique_id, model,  technology=None):
        super().__init__(unique_id, model)
        self.technology = technology
        self.contracts = []
        self.activeContracts = []
        self.collectedFines = 0


    def addContract(self, contract):
        self.contracts.append(contract)
        self.activeContracts.append(contract)

    # simple calculation :
    # TODO : more elaborate calculation
    def calculateFine(self,contract):
        if contract.plasticRate() < contract.minRec :
            return contract.fine
        else:
            return 0


    # collect fines at the end of the contract
    def collectFine(self, contract):
        fine = self.calculateFine(contract)
        if fine > 0 :
            contract.municipality.payFine(fine)
            self.collectedFines += fine


    def makeOffer(self, wasteBase, recTarget):
        minRec = recTarget * random.uniform(0.97,1.03)
        amount = round(wasteBase / 1000 * pricePerTon * random.uniform(0.97,1.03))
        fine = round(amount * 0.1 * random.uniform(0.9,1.1))

        return Offer(self, wasteBase, recTarget, minRec, fine, amount)


    def step(self):
        step = self.model.schedule.steps
        endedContracts = [a for a in self.activeContracts if a.end == step]
        for contract in endedContracts:
            self.collectFine(contract)
            self.activeContracts.remove(contract)






