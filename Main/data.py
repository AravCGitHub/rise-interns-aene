import pandas as pd
import numpy as np
import advertiser
import impression

#reading the data
def read_data(file_path = '/Users/aravchadha/Documents/GitHub/rise-interns-aene/Other/data.txt'):
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

    #find n dim of xmatrix
    return df_filtered, advNum, int(df['Impression'].max())

#creating the matrix
def createWeightMatrix(df, advNum, maxImpId):
    # tempN = maxImpId + 1
    tempN = 1000000 # TODO fix this using maxImpId
    weightMatrix = np.zeros((advNum, tempN))
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

def bigData():
    dataset = read_data()
    df, advNum, maxImpId = dataToDF(dataset, 4)
    weights, impNum = createWeightMatrix(df, advNum, maxImpId)
    print(impNum)
    return advNum, impNum, weights
