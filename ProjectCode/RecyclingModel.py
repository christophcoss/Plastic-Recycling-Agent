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
from Waste import Waste
from Types import *



# metrics
def get_step_number(model):
    return model.schedule.steps

def get_collected_waste(model):
    return get_data_contract(model)[0]

def get_collected_plastic(model):
    return get_data_contract(model)[1]

def get_rate_recycling(model):
    for mun in model.schedule.agents_by_type[Municipality].values():
        return mun.instantRate()

# Assumes one municipality needs to be changed for multiple

def get_rate_recycling_retired(model):
    for mun in model.schedule.agents_by_type[Municipality].values():
        return mun.instantRateType(HouseholdType.RETIRED)

def get_rate_recycling_single(model):
    for mun in model.schedule.agents_by_type[Municipality].values():
        return mun.instantRateType(HouseholdType.SINGLE)

def get_rate_recycling_couple(model):
    for mun in model.schedule.agents_by_type[Municipality].values():
        return mun.instantRateType(HouseholdType.COUPLE)

def get_rate_recycling_family(model):
    for mun in model.schedule.agents_by_type[Municipality].values():
        return mun.instantRateType(HouseholdType.FAMILY)

def get_data_contract(model):
    collectedWaste = 0
    collectedPlastic = 0
    ratePlastic = 0
    for mun in model.schedule.agents_by_type[Municipality].values():
        for contract in mun.contracts:
            collectedWaste   += sum(contract.stepCollectedWaste.values())
            collectedPlastic += sum(contract.stepCollectedPlastic.values())
    if collectedWaste > 0:
        ratePlastic = collectedPlastic / collectedWaste

    return collectedWaste, collectedPlastic, ratePlastic


def get_available_money(model):
    return get_data_municipality(model)[0]

def get_total_fines(model):
    return get_data_municipality(model)[1]

def get_activities_bought(model):
    return get_data_municipality(model)[3]

def get_activity_targeted(model):
    return get_data_municipality(model)[4]

def get_targeted_group(model):
    return get_data_municipality(model)[5]

#Assumes only one municipality
def get_data_municipality(model):
    money = 0
    fines = 0
    for mun in model.schedule.agents_by_type[Municipality].values():
        money += mun.availableMoney
        fines += mun.fines
        rate = mun.rate
        activityBought = mun.activityBought
        activityTargeted = mun.activityTargeted
        targetedGroup = mun.targetedGroup
    return money, fines, rate, activityBought, activityTargeted, targetedGroup


class RecyclingModel(Model):
    def __init__(self, nMunicipality, scenario, seed = None):
        self.config = self.loadConfig()
        super().__init__(seed)
        self.nMunicipality = nMunicipality
        self.nRecComp = self.config["numberOfRecComps"]
        self.nHouseholds = self.config["numberOfHouseholds"]
        self.schedule = RandomActivationByType(self)
        self.scenario = scenario
        self.activities = self.loadActivities()

        #the data collector, defines which variables will be collected, and how
        model_metrics = {
                "step":get_step_number,
                "collectedWaste":get_collected_waste,
                "collectedPlastic":get_collected_plastic,
                "rateRecycling":get_rate_recycling,
                "fines":get_total_fines,
                "availableMoney":get_available_money,
                "activityBought":get_activities_bought,
                "activityTargeted":get_activity_targeted,
                "targetedGroup":get_targeted_group,
                "rateRecyclingRetired": get_rate_recycling_retired,
                "rateRecyclingSingle": get_rate_recycling_single,
                "rateRecyclingCouple": get_rate_recycling_couple,
                "rateRecyclingFamily": get_rate_recycling_family
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
            lHouseholds = mun.setPopulationPerType()
            # First Municipality must be added to schedule before any Household => step by type is
            # called first to Municipality then Household => contracts are created before they are needed
            self.schedule.add(mun)

            # add Households for this municipality
            # recycling available to households
            pAccess = random.uniform(self.config['accessProportion']['Min'], self.config['accessProportion']['Max'])
            access = np.random.choice([True, False], mun.nbHouseholds,p = [pAccess, 1 - pAccess])
            # collection at Home or not
            pAtHome = random.uniform(self.config['partAtHome']['Min'], self.config['partAtHome']['Max'])
            atHome = [True] * mun.nbHouseholds if mun.nbContrat == 1 else \
                list(np.random.choice([True,False], mun.nbHouseholds, p=[pAtHome, 1 - pAtHome]))
            # distance from centralized collection
            lDistance = list(map(lambda x : min(self.config['distanceToCenter']['Max'], max( 0, round(x))), \
                                 np.random.normal(self.config['distanceToCenter']['Mean'],self.config['distanceToCenter']['Var'],mun.nbHouseholds)))

            # recPerception, recImportance and recKnowledge for each HouseholdType
            indexRec = {
                'recPerception' : 0,
                'recImportance' : 1,
                'recKnowledge'  : 2
            }

            distRec = [[0] * len(indexRec) for i in range (len(HouseholdType))]
            for pop in mun.population:
                values = self.config['households'][pop[0].value]
                for rec in indexRec.keys() :
                    distRec[HouseholdType.get_index(pop[0])][indexRec[rec]] = \
                        np.random.normal(values[rec]['Mean'], values[rec]['Var'], pop[1])

            # creation of Households
            indTypes = [0] * len(HouseholdType)
            for j, type in enumerate(lHouseholds):
                i = HouseholdType.get_index(type)
                house = Household(munId + 1 + j, self, mun, type, access[j], atHome[j], lDistance[j],
                                  self.limitValues(distRec[i][indexRec['recPerception']][indTypes[i]]),
                                  self.limitValues(distRec[i][indexRec['recImportance']][indTypes[i]]),
                                  self.limitValues(distRec[i][indexRec['recKnowledge']] [indTypes[i]]))
                self.schedule.add(house)
                indTypes[i] += 1

            # j = 0
            # for pop in types:
            #     values = self.config['households'][pop[0].value]
            #     gausPer = np.random.normal(values['recPerception']['Mean'], values['recPerception']['Var'], pop[1])
            #     gausImp = np.random.normal(values['recImportance']['Mean'], values['recImportance']['Var'], pop[1])
            #     gausKno = np.random.normal(values['recKnowledge']['Mean'], values['recKnowledge']['Var'], pop[1])
            #
            #     distance = random.gauss(self.config['distanceToCenter']['Mean'], self.config['distanceToCenter']['Var'])
            #     maxDistance = self.config['distanceToCenter']['Max']
            #
            #     distance = 0 if distance < 0 else (maxDistance if distance > maxDistance else distance)
            #
            #     for k in range (pop[1]):
            #         house = Household(munId+1+j, self, mun, pop[0], access[j], atHome[j], distance, self.limitValues(gausPer[k]), self.limitValues(gausImp[k]), self.limitValues(gausKno[k]))
            #         self.schedule.add(house)
            #         j += 1

        return

    def loadActivities(self):
        f = open(self.scenario)
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
        if s > 1:
            return 1
        return s

    def getTarget(self):
        # add 5% every 5 years
        return self.config["recyclingTarget"] + 0.05 * (self.schedule.steps // 60)

    def step(self):
        '''Advance the model by one step.'''
        #collect the model data

        #run the step
        print("step : {}".format(self.schedule.steps))
        self.schedule.step()

        self.afterStep()

        self.datacollector.collect(self)

    def afterStep(self):
        muns = self.schedule.get_agents_of_type(Municipality)

        for mun in muns:
            mun.afterStep()
