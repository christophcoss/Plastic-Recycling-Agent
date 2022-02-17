import random
import math
from mesa import Agent

# from Household import Household
from Activity import Activity
from Contract import Contract
from RecyclingCompany import RecyclingCompany
from Types import HouseholdType, CollectionType
from Util import *
from Waste import Waste

class Municipality(Agent):
    def __init__(self, unique_id, model, recTarget, recBudget, nbContrat, nbHouseholds):
        super().__init__(unique_id, model)
        self.recTarget = recTarget
        self.recBudget = recBudget
        self.availableMoney = recBudget
        # self.activityList = activityList
        self.nbContrat = nbContrat
        self.contracts = []
        self.activeContracts = []
        self.nbHouseholds = nbHouseholds
        self.population = []
        self.setPopulationPerType()
        self.fines = 0


    def chooseOffer(self, listOffers):
        res = []
        for offer in listOffers:
            if (offer.fine < offer.baseWaste / 1000 * 0.1 * pricePerTon and \
                offer.minRec >= self.recTarget):
                res.append(offer)
        if len(res) == 0:
            return None
        res.sort(key = lambda x: x.minRec, reverse = True )
        res.sort(key = lambda x: x.amount )
        return res[0]




    # #TODO
    # def setCollectionRate(self, rate):
    #     return

    def makeActivities(self):
       return


    def newContracts(self, step):
        wasteProdNyears = Waste.trashMunicipality(step, lengthContract*12, self.population)
        marge = 1.015
        wasteToContract = round(wasteProdNyears * marge)
        if self.nbContrat == 1 :
            self.newContract(step,CollectionType.AT_HOME,wasteToContract,1)
        else :
            partAtHome = round(random.uniform(0.51,0.65) * wasteProdNyears * marge)
            self.newContract(step,CollectionType.AT_HOME,partAtHome,1)
            self.newContract(step,CollectionType.CENTRALIZED, wasteToContract - partAtHome,2)


    def newContract(self,step,collType,baseWaste,seq):

        recIncs = self.model.schedule.agents_by_type[RecyclingCompany].values()
        offerOK = None
        while (offerOK is None):
            listOffers = []
            for a in recIncs:
               listOffers.append(a.makeOffer(baseWaste, recyclingTarget))
            offerOK = self.chooseOffer(listOffers)

        # an offer has been choosen
        newContract = Contract(self, offerOK.recCompany, offerOK.amount, offerOK.baseWaste, offerOK.minRec, \
                              collType, step, step+lengthContract*12, offerOK.fine, seq)

        self.contracts.append(newContract)
        self.activeContracts.append(newContract)
        self.availableMoney -= offerOK.amount
        offerOK.recCompany.addContract(newContract)


    def payFine(self, fine):
        self.fines += fine
        self.availableMoney -= fine


    def setPopulationPerType(self):
        infVals = [0.10, 0.20, 0.20, 0.20]
        supVals = [0.25, 0.35, 0.35, 0.35]
        p = list(map(lambda x, y: random.uniform(x, y), infVals, supVals))
        sumCoeff = sum(p)
        dist = list(map(lambda x: round(x / sumCoeff * self.nbHouseholds), p))
        delta = self.nbHouseholds - sum(dist)
        if delta != 0:
            f = round(math.copysign(1, delta))
            i= 0
            while (f * delta > 0):
                dist[i % 4] += f
                i += 1
                delta -= f

        self.population.append((HouseholdType.RETIRED, dist[0]))
        self.population.append((HouseholdType.SINGLE , dist[1]))
        self.population.append((HouseholdType.COUPLE , dist[2]))
        self.population.append((HouseholdType.FAMILY , dist[3]))


    def step(self):
        step = self.model.schedule.steps

        # archive non active contract
        endedContracts = [a for a in self.activeContracts if a.end == step]
        for contract in endedContracts:
            self.activeContracts.remove(contract)

        # create new contracts if needed
        if step % (lengthContract*12) == 0  :
            self.newContracts(step)


        # TODO: add activities if rate of plastic too low