import random
#from collections import defaultdict


from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from Household import Household
from Municipality import Municipality
from RandomActivationByType import RandomActivationByType
from RecyclingCompany import RecyclingCompany
from Util import *
from Waste import Waste



# metrics
def get_step_number(model):
    return model.schedule.steps

def get_collected_waste(model):
    return get_data_contract(model)[0]

def get_collected_plastic(model):
    return get_data_contract(model)[1]

def get_rate_recycling(model):
    return get_data_contract(model)[2]

def get_data_contract(model):
    collectedWaste = 0
    collectedPlastic = 0
    ratePlastic = 0
    for mun in model.schedule.agents_by_type[Municipality].values():
        for contract in mun.contracts:
            collectedWaste   += contract.collectedWaste
            collectedPlastic += contract.collectedPlastic
    if collectedWaste > 0:
        ratePlastic = collectedPlastic / collectedWaste

    return collectedWaste, collectedPlastic, ratePlastic


def get_available_money(model):
    return get_data_municipality(model)[0]

def get_total_fines(model):
    return get_data_municipality(model)[1]

def get_data_municipality(model):
    money = 0
    fines = 0
    for mun in model.schedule.agents_by_type[Municipality].values():
        money += mun.availableMoney
        fines += mun.fines
    return money, fines



class RecyclingModel(Model):
    def __init__(self, nMunicipality, nRecComp, nHouseholds, seed = None):
        super().__init__(seed)
        self.nMunicipality = nMunicipality
        self.nRecComp = nRecComp
        self.nHouseholds = nHouseholds
        self.schedule = RandomActivationByType(self)

        #the data collector, defines which variables will be collected, and how
        model_metrics = {
                "step":get_step_number,
                "collectedWaste":get_collected_waste,
                "collectedPlastic":get_collected_plastic,
                "rateRecycling":get_rate_recycling,
                "fines":get_total_fines,
                "availableMoney":get_available_money
            }
        # agent_metrics = {
        #     "wealth":"wealth"
        # }
        self.datacollector = DataCollector(model_reporters=model_metrics)

        #Create Agents
        # recycling compagnies
        for i in range(self.nRecComp):
            recComp = RecyclingCompany(i, self)
            self.schedule.add(recComp)

        # municipalities
        for i in range(self.nMunicipality):
            munId = i*(self.nHouseholds+1) + self.nRecComp
            mun = Municipality(munId, self, recyclingTarget, moneyDispoPerHousehold * self.nHouseholds, \
                               nbContrat, self.nHouseholds)
            # First Municipality must be added to schedule before any Household => step by type is
            # called first to Municipality then Household => contracts are created before thery are needed
            self.schedule.add(mun)

            # add Households for this municipality
            types = getScrambleArray(mun.population)
            #recycling available to households
            access = getScrambleArrayBin(True, False, random.uniform(0.959, 0.981), mun.nbHouseholds)
            # collection at Home or not
            if mun.nbContrat == 1 :
                atHome = [True] * mun.nbHouseholds
            else :
                atHome = getScrambleArrayBin(True, False, random.uniform(0.70, 0.85), mun.nbHouseholds)

            for j in range(self.nHouseholds):
                distance = random.uniform(0,300)
                house = Household(munId+1+j, self, mun, types[j], access[j], atHome[j], distance, \
                                   random.uniform(recPerception-variation, recPerception+variation),\
                                   random.uniform(recImportance-variation, recImportance+variation),\
                                   random.uniform(recKnowledge-variation, recKnowledge+variation))
                self.schedule.add(house)
        return


    def step(self):
        '''Advance the model by one step.'''
        #collect the model data
        self.datacollector.collect(self)
        #run the step
        self.schedule.step()
