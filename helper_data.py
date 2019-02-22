import pandas as pd

def readData(filename):
    df = pd.read_csv(filename, index_col=0)
    #df.set_index('id', inplace=True)
    return df

def getFoodCategories():
    df = readData("CarbonEmissionsPerServing.csv")
    foodCategories = list(df['Category'].unique())
    return [{'label': foodCategory, 'value': foodCategory} for foodCategory in foodCategories]

def getFoodItems():
    df = readData("CarbonEmissionsPerServing.csv")
    foodItems = list(df['Food'].unique())
    return [{'label': foodItem, 'value': foodItem} for foodItem in foodItems]

def getAgeGroups():
    df = readData("CleanFoodData.csv")
    ageGroups = list(df['Pop_Class'].unique())
    return [{'label': ageGroup, 'value': ageGroup} for ageGroup in ageGroups]