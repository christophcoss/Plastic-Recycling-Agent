from mesa import Model
from RecyclingCompany import RecyclingCompany
from Households import Households
from Municipality import Municipality

class RecyclingModel(Model):
    def __int__(self, nRecComp, nHouseholds):
        self.nRecComp = nRecComp
        self.nHouseholds = nHouseholds
        #Create Agents
        
        a = Municipality(0, self)

        for i in range(self.nRecComp):
            a = RecyclingCompany(i+1, self)

        for i in range(self.nHouseholds):
            a = Households(i+1+self.nRecComp, self)