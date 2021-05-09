import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def linear_model_training(df):
    '''
    This function trains a linear model to rebalance the star rating of restaurants based on encoded_cuisine,
    operational status and kid-friendliness.

    Input: df: restaurant data

    Output: trained linear model for new restaurant score calculation
    '''

    df2 = df.copy()

    # encode cuisine type according to popularity
    df2['short_cuisine'] = [i.split()[0] for i in df2['cuisine']]
    short_cuisine_unique = list(df2['short_cuisine'].unique())
    short_cuisine_full = df2['short_cuisine'].tolist()
    short_cuisine_frequency = [short_cuisine_full.count(i) / len(short_cuisine_full) for i in short_cuisine_unique]
    short_cuisine_dict = {}
    for i in range(len(short_cuisine_unique)):
        short_cuisine_dict[short_cuisine_unique[i]] = short_cuisine_frequency[i]
    df2['encoded_cuisine'] = [short_cuisine_dict[i] for i in df2['short_cuisine']]

    # preprocess kid friendliness feature
    df2['int_good_for_kid'] = df2['good_for_kid'].astype('int')

    # model training
    X = df2[['encoded_cuisine', 'is_open', 'int_good_for_kid']].values
    y = df2['star'].values

    reg = LinearRegression(fit_intercept=True).fit(X, y)
    return reg


def star_calculation(model, df):
    '''
    This function calculates popularity star score for restaurants based on trained linear model.

    Input: model: trained linear model for scoring popularity star score
           df: restaurant data to be scored

    Output: df: dataframe with scored popularity star
    '''

    df2 = df.copy()

    # encode cuisine type according to popularity
    df2['short_cuisine'] = [i.split()[0] for i in df2['cuisine']]
    short_cuisine_unique = list(df2['short_cuisine'].unique())
    short_cuisine_full = df2['short_cuisine'].tolist()
    short_cuisine_frequency = [short_cuisine_full.count(i) / len(short_cuisine_full) for i in short_cuisine_unique]
    short_cuisine_dict = {}
    for i in range(len(short_cuisine_unique)):
        short_cuisine_dict[short_cuisine_unique[i]] = short_cuisine_frequency[i]
    df2['encoded_cuisine'] = [short_cuisine_dict[i] for i in df2['short_cuisine']]

    # preprocess kid friendliness feature
    df2['int_good_for_kid'] = df2['good_for_kid'].astype('int')
    X = df2[['encoded_cuisine', 'is_open', 'int_good_for_kid']].values

    df.rename(columns={"star": "star_old"}, inplace=True)

    # new star score calculation
    df['star'] = [round(i, 1) for i in list(model.predict(X))]

    return df