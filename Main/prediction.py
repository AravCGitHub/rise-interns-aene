import random
import optimal

def createPrediction(advs, imps, weights):
    optSolved, optTimeTaken = (optimal.lpSolve(advs,imps,weights))
    for x in range(len(optSolved)):
        optSolved[x] = round(optSolved[x])
        if optSolved[x] == 1:
            rand = random.randint(1,100)
            if rand <= 10:
                optSolved[x] = 0
    return optSolved.reshape(len(advs), len(imps))