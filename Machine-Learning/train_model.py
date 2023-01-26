import os, json
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm

DATAPATH = os.path.dirname(__file__) + '/data/'

def get_files():
    os.chdir(DATAPATH)
    df = pd.DataFrame()
    for file in glob.glob('*.json'):
        filepath = DATAPATH + file
        opened_df = pd.read_json(filepath)
        df = pd.concat([df, opened_df], ignore_index=True)
    return df

def create_X_y(df):
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
    print(len(df[df["test_y"]!=df.iloc[:,0]])/len(df["test_y"])) #Proportion of correct data to incorrect data. 61% is not an accurate enough prediction.
    


if __name__=='__main__':
    #print("gnu")
    df = get_files()
    data = create_X_y(df)
    train_model_with_logistic_regression(data)
    train_model_with_SVM(data)