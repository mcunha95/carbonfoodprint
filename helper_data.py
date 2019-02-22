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
    food_categories = list(df['Category'].unique())
    return get_dictionary_for_dash(food_categories)


def get_food_items(country, age_group, category):
    df = read_data("df/CleanFoodData.csv")
    df2 = pd.read_csv("df/CO2Footprint.csv", index_col=0)
    if not age_group:
        food_items_by_category = list(df['Food'].unique())
    else:
        food_items = list(df[(df.index == country) & (df['Pop_Class'] == age_group)].FoodId.unique())
        food_items_co2dataset = df2.loc[df2.index.isin(food_items)]
        food_items_by_category = list(food_items_co2dataset[food_items_co2dataset['Category'] == category].Food)
    return get_dictionary_for_dash(food_items_by_category)


def get_dictionary_for_dash(series):
    return [{'label': item, 'value': item} for item in series]
