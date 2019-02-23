import pandas as pd


def read_data(filename):
    df = pd.read_csv(filename, index_col=0)
    return df


def get_countries():
    df = read_data("df/CleanFoodData.csv")
    countries = list(df.index.unique())
    return get_dictionary_for_dash(countries)


def get_age_groups(country):
    df = read_data("df/CleanFoodData.csv")
    age_groups = list(df.loc[country].Pop_Class.unique())
    return get_dictionary_for_dash(age_groups)


def get_food_categories():
    df = read_data("df/CO2Footprint.csv")
    return list(df['Category'].unique())


def get_food_items(country, age_group, category):
    df = read_data("df/CleanFoodData.csv")
    df2 = pd.read_csv("df/CO2Footprint.csv", index_col=0)
    if not country or not age_group:
        food_items_by_category = list(df2[df2['Category'] == category].Food)
    else:
        food_items = list(df[(df.index == country) & (df['Pop_Class'] == age_group)].FoodId.unique())
        food_items_co2dataset = df2.loc[df2.index.isin(food_items)]
        food_items_by_category = list(food_items_co2dataset[food_items_co2dataset['Category'] == category].Food)
    return food_items_by_category


def get_dictionary_for_dash(series):
    return [{'label': item, 'value': item} for item in series]


def get_food_category_and_item_dictionary():
    newDict = {}
    food_categories = get_food_categories()
    for category in food_categories:
        newDict[category] = get_food_items('','',category)
    return newDict
    
def get_slider_box_keys():
    keys = []
    categories = get_food_categories()
    for category in categories:
        subList = get_food_items('','',category)
        structuredSubList = ['slider-'+category+'-'+foodItem for foodItem in subList]
        keys = keys + structuredSubList
    return keys
