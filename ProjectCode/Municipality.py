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

# Municipality is another very important agent (for now there are only one but can run the model with more)
# - They have a recycling target in %
# - They have a recycling budget (for now for the full 20 years, need to modify to be yearly)
# - They have a number of contracts (with recycling companies for trash collection and recycling)
# - They have a number of households (which are responsible for producing the trash)

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
        self.stepTotalCollectedWaste = 0
        self.stepTotalCollectedPlastic = 0
        self.rate = 0
        self.pendingActivities = []
        self.activityBought = 'None'
        self.rateOfTypes = {"retired": 0, "single": 0, "couple": 0, "family": 0}


    # The municipality receives offers from multiple companies it needs to choose only one.
    # does so by eliminating companies that have unrealistic fines and realistic recycling targets,
    # then chooses the cheapest with the highest recycling target
    # returns none if there are no suitable offer
    # NEED TO REVISE MIGHT BE WRONG
    def chooseOffer(self, listOffers):
        res = []
        for offer in listOffers:
            if (offer.fine < offer.baseWaste / 1000 * 0.1 * self.model.config['pricePerTon'] and \
                offer.minRec >= self.model.getTarget()):
                res.append(offer)
        if len(res) == 0:
            return None
        res.sort(key = lambda x: x.minRec, reverse = True )
        res.sort(key = lambda x: x.amount )
        return res[0]


    # Municipalities must use their left over yearly budget to create activities (PR campaign for example)
    # that will improve the preception, importance and knowledge of the households towards recycling.
    def getActivity(self, name):
        for act in self.model.activities:
            if act.name == name:
                return act

    def makeActivities(self):
        #activityValue = 0


        lowestPerformingType = min(self.rateOfTypes, key=self.rateOfTypes.get)
        act = None
        if lowestPerformingType == HouseholdType.FAMILY.value:
            act = self.getActivity("educative events on recycling importance")
        if lowestPerformingType == HouseholdType.RETIRED.value:
            act = self.getActivity("Billboard campaign on recycling importance")
        if lowestPerformingType == HouseholdType.SINGLE.value:
            act = self.getActivity("Digital campaign on recycling importance")
        if lowestPerformingType == HouseholdType.COUPLE.value:
            act = self.getActivity("Digital campaign on recycling importance")


        ## need to add that if the differences of rates between each category is too low then just build more collection spots or smth like that

        if act.totalCost(self.nbHouseholds) < (self.availableMoney / 2):
            act.effectOnStep = act.stepsToEffect + self.model.schedule.steps
            self.pendingActivities.append(act)
            self.activityBought = act.name
            self.availableMoney -= act.totalCost(self.nbHouseholds)


            # activities.sort(key = lambda x: (x.relativeEfficiency(self.population, self.nbHouseholds), x.totalCost(self.nbHouseholds)), reverse = True)
        # for act in activities:
        #     if act.totalCost(self.nbHouseholds) < (self.availableMoney/2):
        #         act.effectOnStep = act.stepsToEffect + self.model.schedule.steps
        #         self.pendingActivities.append(act)
        #         self.activityBought = act.name
        #         self.availableMoney -= act.totalCost(self.nbHouseholds)
        #         break
        # return


    # Decide how many new contracts need to be made for the coming (3) years
    def newContracts(self, step):
        wasteProdNyears = Waste.trashMunicipality(step, self.model.config['lengthContract']*12, self.population)
        margin = 1.015
        wasteToContract = round(wasteProdNyears * margin)
        if self.nbContrat == 1 :
            self.newContract(step,CollectionType.AT_HOME,wasteToContract,1)
        else :
            partAtHome = round(random.uniform(self.model.config['partAtHome']['Min'],self.model.config['partAtHome']['Max']) * wasteProdNyears * margin)
            self.newContract(step,CollectionType.AT_HOME,partAtHome,1)
            self.newContract(step,CollectionType.CENTRALIZED, wasteToContract - partAtHome,2)

    # create a new contrat with a recycling company
    def newContract(self,step,collType,baseWaste,seq):

        recIncs = self.model.schedule.agents_by_type[RecyclingCompany].values()
        offerOK = None
        while (offerOK is None):
            listOffers = []
            for a in recIncs:
               listOffers.append(a.makeOffer(baseWaste, self.model.getTarget()))
            offerOK = self.chooseOffer(listOffers)

        # an offer has been chosen
        newContract = Contract(self, offerOK.recCompany, offerOK.amount, offerOK.baseWaste, offerOK.minRec, \
                              collType, step, step+self.model.config['lengthContract']*12, offerOK.fine, seq)

        self.contracts.append(newContract)
        self.activeContracts.append(newContract)
        self.availableMoney -= offerOK.amount
        offerOK.recCompany.addContract(newContract)


    def payFine(self, fine):
        self.fines += fine
        self.availableMoney -= fine



    # Municipality needs to create its population this is done in a semi-random way
    # where interval is given for the proportion of a certain household type in the municipality
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
        self.population.append((HouseholdType.SINGLE, dist[1]))
        self.population.append((HouseholdType.COUPLE, dist[2]))
        self.population.append((HouseholdType.FAMILY, dist[3]))


    def step(self):
        step = self.model.schedule.steps

        # archive non active contract
        endedContracts = [a for a in self.activeContracts if a.end == step]
        for contract in endedContracts:
            self.activeContracts.remove(contract)

        # create new contracts if needed
        if step % (self.model.config['lengthContract']*12) == 0:
            self.newContracts(step)


    def afterStep(self):
        self.rate = self.instantRate()
        self.getRatesPerType()
        # maybe change this so that it takes into account avoiding fines from companies
        if self.rate < (self.model.getTarget() * 1.05) and self.model.schedule.steps % 12 == 0 and self.model.schedule.steps != 0:
            self.makeActivities()
        else:
            self.activityBought = 'None'

    def instantRate(self) :
        self.stepTotalCollectedWaste = 0
        self.stepTotalCollectedPlastic = 0
        for contract in self.activeContracts:
            self.stepTotalCollectedWaste += sum(contract.stepCollectedWaste.values())
            self.stepTotalCollectedPlastic += sum(contract.stepCollectedPlastic.values())
        rate = 0 if self.stepTotalCollectedWaste == 0 else self.stepTotalCollectedPlastic / (self.stepTotalCollectedWaste * self.model.config['plasticRateInWaste'])
        if rate > 1: print("error at step " + str(self.model.schedule.steps))
        return rate

    def instantRateType(self, houseHoldType):
        typeCollectedWaste = 0
        typeCollectedPlastic = 0
        for contract in self.activeContracts:
            typeCollectedPlastic += contract.stepCollectedPlastic[houseHoldType.value]
            typeCollectedWaste += contract.stepCollectedWaste[houseHoldType.value]
        return 0 if typeCollectedWaste == 0 else typeCollectedPlastic / (typeCollectedWaste * self.model.config['plasticRateInWaste'])

    def getRatesPerType(self):
        for type in HouseholdType:
            self.rateOfTypes[type.value] = self.instantRateType(type)
