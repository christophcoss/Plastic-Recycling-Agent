import random
from mesa import Agent

from Offer import Offer
from Util import *
from Types import *
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
        if contract.globalPlasticRate() < contract.minRec :
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
        conTargetD = self.model.config['contractTargetDelta']
        conPriceD = self.model.config['contractPriceDelta']
        fineFactor = self.model.config['fineFactor']['factor']
        fineFactorD = self.model.config['fineFactor']['delta']
        minRec = recTarget * random.uniform(1 - conTargetD,1 + conTargetD)
        amount = round(wasteBase / 1000 * self.model.config['pricePerTon'] * random.uniform(1 - conPriceD,1 + conPriceD))
        fine = round(amount * fineFactor * random.uniform(1 - fineFactorD,1 + fineFactorD))

        return Offer(self, wasteBase, recTarget, minRec, fine, amount)

    def resetCollectedWaste(self):
        for con in self.activeContracts:
            for type in HouseholdType:
                con.stepCollectedWaste[type.value] = 0
                con.stepCollectedPlastic[type.value] = 0

    def step(self):
        self.resetCollectedWaste()
        step = self.model.schedule.steps
        endedContracts = [a for a in self.activeContracts if a.end == step]
        for contract in endedContracts:
            self.collectFine(contract)
            self.activeContracts.remove(contract)






