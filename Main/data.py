import pandas as pd
import numpy as np
import advertiser
import impression
from synInst import createAdvsAndImps

#reading the data
def read_data(file_path = 'Main/data.txt'):
    data = []
    file = open(file_path, 'r', encoding='utf-8')
    for line in file:
        data.append(line.strip().split('\t'))
    return data

#converting data into dataframe
def dataToDF(data, advNum):
    advs = []
    imps = []
    weights = []
    currAdv = ""
    advCount = 0
    for line in data:
        if line[0] == 'U':
            currAdv = line[1]
            advCount += 1
        elif line[0] == 'V':
            imps.append(line[2])
            advs.append(currAdv)
            weights.append(line[1])

        if advCount >= advNum:
            break
    # file = open("demofile3.txt", "r")
    # print(file.read())

    #drop duplicates
    df = pd.DataFrame({'Advertiser': advs, 'Impression': imps, 'Weight': weights}, index=(a for a in range(len(advs))))
    mask = df['Impression'].isin(df['Advertiser'])
    df_filtered = df[~mask]
    maxImpId = df_filtered['Impression'].astype(int).max() + 1

    #find n dim of xmatrix
    return df_filtered, maxImpId

#creating the matrix
def createWeightMatrix(df, advNum, maxImpId):
    weightMatrix = np.zeros((advNum, maxImpId))
    currAdv = df['Advertiser'][1]
    count = 0
    for index, row in df.iterrows():
        if currAdv != row['Advertiser']:
            currAdv = row['Advertiser']
            count += 1
        weightMatrix[count][int(row['Impression'])] = row['Weight']

    droppedColumns = [] 
    for i in range(len(weightMatrix[0])):
        if np.array_equal(weightMatrix[:,i], np.zeros(advNum)):
            droppedColumns.append(i)

    weightMatrix = np.delete(weightMatrix, droppedColumns, axis=1)
    impNum = weightMatrix.shape[1]
    return weightMatrix.ravel().tolist(), impNum

def giveWeights(weightMatrix, impsList):
    for i in range(len(impsList)):
        impsList[i].weight = weightMatrix[i]


def formatBigData(advNum):
    dataset = read_data()
    df, maxImpId = dataToDF(dataset, advNum)
    weights, impNum = createWeightMatrix(df, advNum, maxImpId)
    advsList, impsList = createAdvsAndImps(advNum, impNum)
    giveWeights(weights, impsList)
    return advsList, impsList, weights
