import os, json
import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.metrics import r2_score

DATAPATH = os.path.dirname(__file__) + '/data/'

def get_files():
    os.chdir(DATAPATH)
    df = pd.DataFrame()
    for file in glob.glob('*.json'):
        filepath = DATAPATH + file
        opened_df = pd.read_json(filepath)
        df = pd.concat([df, opened_df], ignore_index=True)
    return df

def create_X_y_for_classification(df):
    """
    Input: Pandas DataFrame
    Output: Dictionary of Numpy-arrays to use in regression model.

    Uses the function train_test_split from sklearn-library:
    Takes in X,y as variables, sets a test-size, a random_state and returns 2 DataFrames for X and 2 Series for y
    test_size decides the proportion of our test-data to training data.
    random_state I understand it as setting a static randomization between tries. So the randomized train and test data is equal between runs.
    """
    #print(df.columns)
    X = df.drop('description_index', axis=1)
    y = df["description_index"]
    train_X, test_X, train_y,test_y = train_test_split(X,y,test_size=0.3, random_state=42)
    data = {
        "train_X": train_X,
        "train_y": train_y,
        "test_X": test_X,
        "test_y": test_y
    }
    #print(type(train_X))
    return data

def create_X_y_for_linear_regression(df):
    """
    Input: Pandas DataFrame
    Output: Dictionary of Numpy-arrays to use in regression model.

    Uses the function train_test_split from sklearn-library:
    Takes in X,y as variables, sets a test-size, a random_state and returns 2 DataFrames for X and 2 Series for y
    test_size decides the proportion of our test-data to training data.
    random_state I understand it as setting a static randomization between tries. So the randomized train and test data is equal between runs.
    """
    print(df.columns)
    df = df.drop('description_index', axis=1)
    X=df.drop(['temperature'], axis=1)
    y = df["temperature"]
    train_X, test_X, train_y,test_y = train_test_split(X,y,test_size=0.3, random_state=42)
    data = {
        "train_X": train_X,
        "train_y": train_y,
        "test_X": test_X,
        "test_y": test_y
    }
    #print(type(train_X))
    return data


def train_model_with_linear_regression(data):
    cls = LinearRegression()
    cls.fit(data["train_X"], data["train_y"])
    y_pred = cls.predict(data["test_X"])
    df = pd.DataFrame(y_pred)
    df["test_y"] = data["test_y"].values
    df.columns = ["pred_y","test_y"]
    r2 = r2_score(df["test_y"],df["pred_y"].round())

    print(df,r2)
    
    # Get r2 = 0.3244 without changes.
    # If I remove wind_speed I get r2 = 0.017 which is a significantly lower number
    # I therefore assume wind_speed may have an association with temperature.
    # Removing air_pressure and humidity both lowered r2. If I removed both r2 = 0.289.
    # As expected, making temperature one of the predictors for temperature increased r2 to 0.99 which is practically perfect.


def train_model_with_logistic_regression(data):
    cls = LogisticRegression()
    cls.fit(data["train_X"], data["train_y"])
    cls.set_params(max_iter=6000)

    y_prediction = cls.predict(data["test_X"])
    df = pd.DataFrame(y_prediction)
    df["test_y"] = data["test_y"].values

    print(data["test_y"])
    print(df)
    print(type(y_prediction))

def train_model_with_SVM(data):
    clf = svm.SVC()
    clf.fit(data["train_X"], data["train_y"])
    y_pred = clf.predict(data["test_X"])
    df = pd.DataFrame(y_pred)
    df["test_y"] = data["test_y"].values
    df.columns=["pred_y","test_y"]
    print(len(df[df["test_y"]!=df.iloc[:,0]])/len(df["test_y"])) #Proportion of correct data to incorrect data. 61% is not an accurate enough prediction.
    


if __name__=='__main__':
    #print("gnu")
    df = get_files()
    data = create_X_y_for_classification(df)
    data = create_X_y_for_linear_regression(df)
    #train_model_with_logistic_regression(data)
    #train_model_with_SVM(data)
    train_model_with_linear_regression(data)