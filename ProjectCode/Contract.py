from Types import CollectionType

#Contract is between municipality and recycling company. The contract indicates:
# - the total price of the contract,
# - the quantity of base waste,
# - the minimum percentage of plastic recycling
# - the type of collection (at home or centralized)
# - the start time (step #)
# - the end time (step #)
# - the fine, the recycling company can fine the municipality if not enough plastic waste is collected
# - sequence number (identification)

class Contract:
    def __init__(self,municipality, recCompagny, amount, baseWaste, minRec, type, start, end, fine, seq):
        self.municipality = municipality
        self.recCompagny = recCompagny
        self.num = "C{:03d}_{:03d}_{:03d}_{:02d}".format(municipality.unique_id, recCompagny.unique_id,start,seq)
        self.baseWaste = baseWaste
        self.amount = amount
        self.minRec = minRec
        self.type = type
        self.start = start
        self.end = end
        self.fine = fine
        self.collectedWaste = 0
        self.collectedPlastic = 0
        self.stepCollectedWaste = 0
        self.stepCollectedPlastic = 0
        self.full = False


    def collect(self, wasteNPlasticToThrow, wastePlasticToThrow) :
        avail = self.baseWaste - self.collectedWaste
        wasteToThrow = wastePlasticToThrow + wasteNPlasticToThrow
        if self.full :
            return wasteNPlasticToThrow, wastePlasticToThrow
        if avail >= wasteToThrow:
            self.collectedWaste += wasteToThrow
            self.stepCollectedWaste += wasteToThrow
            self.collectedPlastic += wastePlasticToThrow
            self.stepCollectedPlastic += wastePlasticToThrow
            return 0 , 0
        else:
            self.full = True
            plastic = self.wastePlasticToThrow * avail / wasteToThrow
            nonPlastic = self.wasteNPlasticToThrow * avail / wasteToThrow
            self.collectedWaste += avail
            self.stepCollectedWaste += avail
            self.collectedPlastic += plastic
            self.stepCollectedPlastic += plastic
            return wasteNPlasticToThrow - nonPlastic , wastePlasticToThrow - plastic


    # % of plastic waste recycled from total waste
    def globalPlasticRate(self):
        if self.collectedWaste == 0 :
            return 1
        else :
            return self.collectedPlastic / self.collectedWaste




