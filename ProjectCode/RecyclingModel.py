import random
import json
import numpy as np

#from collections import defaultdict


from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from Activity import Activity
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
    return get_data_municipality(model)[2]

def get_data_contract(model):
    collectedWaste = 0
    collectedPlastic = 0
    ratePlastic = 0
    for mun in model.schedule.agents_by_type[Municipality].values():
        for contract in mun.contracts:
            collectedWaste   += contract.stepCollectedWaste
            collectedPlastic += contract.stepCollectedPlastic
    if collectedWaste > 0:
        ratePlastic = collectedPlastic / collectedWaste

    return collectedWaste, collectedPlastic, ratePlastic


def get_available_money(model):
    return get_data_municipality(model)[0]

def get_total_fines(model):
    return get_data_municipality(model)[1]

#Assumes only one municipality
def get_data_municipality(model):
    money = 0
    fines = 0
    for mun in model.schedule.agents_by_type[Municipality].values():
        money += mun.availableMoney
        fines += mun.fines
        rate = mun.rate
    return money, fines, rate


class RecyclingModel(Model):
    def __init__(self, nMunicipality, nRecComp, nHouseholds, seed = None):
        super().__init__(seed)
        self.activities = self.loadActivities()
        self.nMunicipality = nMunicipality
        self.nRecComp = nRecComp
        self.nHouseholds = nHouseholds
        self.schedule = RandomActivationByType(self)
        self.config = self.loadConfig()


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
        #         "rate":getRate
        #     }
        self.datacollector = DataCollector(model_reporters=model_metrics)

        #Create Agents
        # recycling compagnies
        for i in range(self.nRecComp):
            recComp = RecyclingCompany(i, self)
            self.schedule.add(recComp)

        # municipalities
        for i in range(self.nMunicipality):
            munId = i*(self.nHouseholds+1) + self.nRecComp
            mun = Municipality(munId, self, self.getTarget(), self.config['moneyDispoPerHousehold'] * self.nHouseholds, \
                               self.config['nBContract'], self.nHouseholds)
            # First Municipality must be added to schedule before any Household => step by type is
            # called first to Municipality then Household => contracts are created before thery are needed
            self.schedule.add(mun)

            # add Households for this municipality
            types = mun.population
            #recycling available to households
            access = getScrambleArrayBin(True, False, random.uniform(self.config['accessProportion']['Min'], self.config['accessProportion']['Max']), mun.nbHouseholds)
            # collection at Home or not
            if mun.nbContrat == 1 :
                atHome = [True] * mun.nbHouseholds
            else :
                atHome = getScrambleArrayBin(True, False, random.uniform(0.70, 0.85), mun.nbHouseholds)


            j = 0
            for pop in types:
                values = self.config['households'][pop[0].value]
                gausPer = np.random.normal(values['recPerception']['Mean'], values['recPerception']['Var'], pop[1])
                gausImp = np.random.normal(values['recImportance']['Mean'], values['recImportance']['Var'], pop[1])
                gausKno = np.random.normal(values['recKnowledge']['Mean'], values['recKnowledge']['Var'], pop[1])

                distance = random.gauss(self.config['distanceToCenter']['Mean'], self.config['distanceToCenter']['Var'])
                maxDistance = self.config['distanceToCenter']['Max']

                distance = 0 if distance < 0 else (maxDistance if distance > maxDistance else distance)

                for k in range (pop[1]):
                    house = Household(munId+1+j, self, mun, pop[0], access[j], atHome[j], distance, self.limitValues(gausPer[k]), self.limitValues(gausImp[k]), self.limitValues(gausKno[k]))
                    self.schedule.add(house)
                    j += 1

        return

    def loadActivities(self):
        f = open('Activities.json')
        data = json.load(f)
        f.close()
        res = []
        for a in data:
            act = Activity(a)
            res.append(act)
        return res

    def loadConfig(self):
        f = open('config.json')
        data = json.load(f)
        f.close()
        Waste.init(data)
        return data

    def limitValues(self, s):
        if s < 0:
            return 0
        if s < 1:
            return s
        return 1

    def getTarget(self):
        # add 5% every 5 years
        return self.config["recyclingTarget"] + 0.05 * (self.schedule.steps // 60)

    def step(self):
        '''Advance the model by one step.'''
        #collect the model data
        if self.schedule.steps != 0:
            self.datacollector.collect(self)
        #run the step
        self.schedule.step()

        self.afterStep()

    def afterStep(self):
        muns = self.schedule.get_agents_of_type(Municipality)

        for mun in muns:
            mun.afterStep()
