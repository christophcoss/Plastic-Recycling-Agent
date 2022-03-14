import random





def getScrambleArray(pairs):
    res = []
    for pair in pairs:
        res.extend([pair[0]] * pair[1])
    # return sorted(res, key=lambda x: random.random())
    random.shuffle(res)
    return res

def getScrambleArrayBin(val1,val2,perCent1,totalQ):
    n1 = round(perCent1*totalQ)
    n2 = totalQ-n1
    return getScrambleArray([(val1,n1),(val2,n2)])

