from Types import CollectionType


class Offer:
    def __init__(self, recCompagny, baseWaste, recTarget, minRec, fine, amount):
        self.recCompany = recCompagny
        self.baseWaste = baseWaste
        self.recTarget = recTarget
        self.minRec = minRec
        self.fine = fine
        self.amount = amount
