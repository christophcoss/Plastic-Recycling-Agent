from Types import CollectionType

# Recycling Companies need to make offers to the municipality for their services such that the municipality can choose which companies to hire.
class Offer:
    def __init__(self, recCompagny, baseWaste, recTarget, minRec, fine, amount):
        self.recCompany = recCompagny
        self.baseWaste = baseWaste
        self.recTarget = recTarget
        self.minRec = minRec
        self.fine = fine
        self.amount = amount
