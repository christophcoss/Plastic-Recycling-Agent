from mesa import Model

class RecyclingModel(Model):
    def __int__(self, nRecComp, nHouseholds):
        self.nRecComp = nRecComp
        self.nHouseholds = nHouseholds
        