import sqlalchemy
import pandas as pd
import os
import datetime
import json

DATADIR = os.path.dirname(__file__) + '/data/'
print(DATADIR)

with open(os.path.dirname(__file__) + '/login.txt', 'r') as fh:
    params = eval(fh.read())
enginestring = f"""postgresql://{params["user"]}:{params["password"]}@{params["host"]}:{params["port"]}/{params["database"]}"""
engine = sqlalchemy.engine.create_engine(enginestring)

def get_sql_data(engine):
    """
    Gets SQL data based on the string in query.
    Input: engine (sqlalchemy engine)
    Output: pandas DataFrame
    """
    query = """
    SELECT * FROM weather_data;
    """
    df = pd.read_sql(query, engine)
    return df

def extract_desired_columns(df):
    """
    Input: Pandas DataFrame
    Output: Pandas DataFrame with the columns:
   "msl", "t", "r", "ws" and "wsymb2" for weather description."""
    df = df[["msl_value","t_value","ws_value", "r_value","wsymb2_value"]]
    df.columns = ["air_pressure","temperature","wind_speed","humidity","description_index"]
    return df

def dump_to_json(df):
    #fh = open(os.path.dirname(__file__) + '/data/data' + datetime.datetime.now().strftime('%Y-%m-%d-%H') +'.json', 'w')
    print(df)
    js = df.to_json(os.path.dirname(__file__) + '/data/data' + datetime.datetime.now().strftime('%Y-%m-%d-%H') +'.json')
    #json.dump(js,fh)
    #fh.close()

if __name__ == '__main__':
    df = get_sql_data(engine)
    df = extract_desired_columns(df)
    dump_to_json(df)
