import os
import glob
import sqlalchemy
import pandas as pd

precipitationon_desc = {
    "id": list(range(1, 8)),
    "precipitation": ["No precipitation", "Snow", "Snow and Rain", "Rain", "Drizzle", "Freezing rain", "Freezing drizzle"]
}

# Weather Descriptions
weather_desc = {
    "id": list(range(1, 28)),
    "weather_description": [
        "Clear sky", "Nearly clear sky", "Variable cloudiness", "Halfclear sky", "Cloudy sky",
        "Overcast", "Fog", "Light rain showers", "Moderate rain showers", "Heavy rain showers",
        "Thunderstorm", "Light sleet showers", "Moderate sleet showers", "Heavy sleet showers",
        "Light snow showers", "Moderate snow showers", "Heavy snow showers", "Light rain", "Moderate rain",
        "Heavy rain", "Thunder", "Light sleet", "Moderate sleet", "Heavy sleet",
        "Light snowfall", "Moderate snowfall", "Heavy snowfall"
    ]
}

# Cloud Cover Descriptions

cloud_cover_desc = {
    "id": list(range(1, 5)),
    "params": [
        "tcc_mean", "lcc_mean", "mcc_mean", "hcc_mean"
    ],
    "desc": [
        "The total cloud cover. How big part of the sky is covered by clouds.",
        "Low cloud cover. Clouds between 0 and 2500 meters.",
        "Medium cloud cover. Clouds between 2500 and 6000 meters.",
        "High cloud cover. Clouds above 6000 meters."
    ]
}
# Local refs
ROOTPATH = os.path.dirname(os.path.dirname(__file__))
CLEANEDPATH = ROOTPATH + '/data/testing/cleaned/'
SQLPATH = ROOTPATH + '/cleansed_to_sql/'
with open(os.path.dirname(__file__) + '/login.txt', 'r') as f:
    params = eval(f.read())
enginestring = f"""postgresql://{params["user"]}:{params["password"]}@{params["host"]}:{params["port"]}/{params["database"]}"""
engine = sqlalchemy.create_engine(enginestring)


def date_table(df):
    d_time = pd.DataFrame(df["time"])
    d_time.drop_duplicates(inplace=True)
    d_time = convert_datetime(d_time)
    d_time['year'] = d_time['time'].apply(lambda x: x.year)
    d_time['month'] = d_time['time'].apply(lambda x: x.month)
    d_time["day"] = d_time['time'].apply(lambda x: x.day)
    d_time["hour"] = d_time["time"].apply(lambda x: x.hour)
    return d_time


def initialize_db():
    if not sqlalchemy.inspect(engine).has_table("precipitation_category"):
        create_pcat_table().to_sql('precipitation_category', engine)
    if not sqlalchemy.inspect(engine).has_table("city"):
        create_city_table().to_sql('city', engine)
    if not sqlalchemy.inspect(engine).has_table("weather_description"):
        create_weather_table().to_sql('weather_description', engine)
    if not sqlalchemy.inspect(engine).has_table("cloud_cover_description"):
        create_cloud_cover_table().to_sql('cloud_cover_description', engine)
    if not sqlalchemy.inspect(engine).has_table('weather_data'):
        df = pd.read_json(SQLPATH+'template.txt')
        df = convert_datetime(df)
        df = create_unit_table(df)
        df = df[df["time"].isin(["häst"])]
        df.to_sql('weather_data', engine)
    return True


def create_unit_table(df):
    unit_df = df.filter(like='_unit', axis=1)
    if unit_df.empty:
        return df
    unit_values = unit_df.iloc[1, :]
    unit_value_df = pd.DataFrame(unit_values).reset_index()
    unit_value_df.index += 1
    unit_value_df.columns = ["value", "unit"]
    for item in unit_df.columns:
        df[item] = df[item].replace(
            unit_value_df[unit_value_df["value"] == item].index.values)
    df.drop(unit_df.columns, axis=1, inplace=True)

    unit_value_df.to_sql('unit', engine, if_exists='replace')
    return df


def create_pcat_table():
    df = pd.DataFrame(precipitationon_desc)
    df.set_index("id", inplace=True)
    return df


def create_weather_table():
    df1 = pd.DataFrame(weather_desc)
    return df1


def create_cloud_cover_table():
    df2 = pd.DataFrame(cloud_cover_desc)
    return df2


def create_city_table():
    df = pd.read_json(SQLPATH + '/cities.txt')
    df.reset_index(inplace=True)
    df.set_index("city_id", inplace=True)
    print(df)
    return df


def file_in_log_file(file):
    if not os.path.exists(SQLPATH + 'data_inserted.txt'):
        return True
    with open(SQLPATH+'data_inserted.txt', 'r') as fh:
        filelist = fh.read().split(',')
        if file in filelist:
            return False
        else:
            return True


def save_logfile(file):
    if not os.path.exists(SQLPATH + 'files_posted_to_database.txt'):
        with open(SQLPATH+'files_posted_to_database.txt', 'w') as fh:
            fh.write('')  # Nuvarande variant fungerar.
    with open(SQLPATH+'files_posted_to_database.txt', 'r') as fh:
        filelist = fh.read().split(',')
    if file not in filelist:
        with open(SQLPATH+'files_posted_to_database.txt', 'a') as f:
            f.write(file + ',')


def file_not_in_log_file(file):
    if not os.path.exists(SQLPATH + 'files_posted_to_database.txt'):
        return True
    with open(SQLPATH+'files_posted_to_database.txt', 'r') as fh:
        filelist = fh.read().split(',')
        if file in filelist:
            return False
        else:
            return True


def convert_datetime(df):
    df["time"] = pd.to_datetime(df["time"], format='%Y-%m-%dT%H:%M:%S')
    return df


def remove_already_inserted_values_from_dataframe(df):
    time = pd.read_sql("weather_data", engine)["time"]
    time = time.dt.strftime('%Y-%m-%d %H:%M:%S')
    df["time"] = df["time"].dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df[~df["time"].isin(time)]
    return df


def create_main_dataframe():
    os.chdir(CLEANEDPATH)
    df = pd.DataFrame()
    for file in glob.glob('*.json'):
        if os.path.exists(SQLPATH+'files_posted_to_database.txt'):
            with open(SQLPATH+'files_posted_to_database.txt', 'r') as fh:
                if file in fh.read().split(','):
                    continue
        filepath = CLEANEDPATH + file
        df = pd.concat([df, pd.read_json(filepath)], ignore_index=True)
        save_logfile(file)
    if not df.empty:
        df = convert_datetime(df)
        df = remove_already_inserted_values_from_dataframe(df)
        df = create_unit_table(df)
    return df


def write_sql():
    initialize_db()
    df = create_main_dataframe()
    if not df.empty:
        date_tables = date_table(df)
        date_tables.to_sql('time', engine, if_exists='append')
        df.to_sql('weather_data',engine,if_exists="append")


if __name__ == '__main__':
    write_sql()
    print(pd.read_sql('weather_data', engine))