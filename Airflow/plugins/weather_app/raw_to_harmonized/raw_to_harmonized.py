import os, glob, datetime, numpy, re
import pandas as pd
import json

# Local refs
ROOTPATH = os.path.dirname(os.path.dirname(__file__))
RAWPATH = ROOTPATH + '/data/testing/raw/'
HARMONIZEDPATH = ROOTPATH + '/data/testing/harmonized/'
SQLPATH = ROOTPATH + '/cleansed_to_sql/'
# dict_keys(['approvedTime', 'referenceTime', 'geometry', 'timeSeries']

# Trasforming/Harmonizing the raw data, and create DataFrame(s)
def harmonize_dict(js):
    js = js["timeSeries"]
    harmonized_dict = {}
    harmonized_unit_dict = {}

    for dictitem in js:
        harmonized_dict["time"] = harmonized_dict.get("time", [])
        harmonized_dict["time"].append(dictitem["validTime"])
        harmonized_unit_dict["time"] = harmonized_unit_dict.get("time", [])
        harmonized_unit_dict["time"].append(dictitem["validTime"])

        for item in dictitem["parameters"]:
            item["values"] = item["values"][0]
            harmonized_dict[item["name"].lower() + '_value'] = harmonized_dict.get(item["name"].lower() + "_value", [])
            harmonized_dict[item["name"].lower() + '_value'].append(item["values"])
            harmonized_unit_dict[item["name"].lower() + '_unit'] = harmonized_unit_dict.get(item["name"].lower() + "_unit", [])
            harmonized_unit_dict[item["name"].lower() + '_unit'].append(item["unit"])
    
    for key, value in harmonized_unit_dict.items():
        harmonized_dict[key] = harmonized_dict.get(key, value)
    
    df = pd.DataFrame(harmonized_dict)
    return df

# Sort columns in dataframe to show parameter value and unit, change so time is still first column
def sort_columns(df):
    sortedlist = sorted(df.columns)
    sortedlist.remove("time")
    sortedlist = ["time", *sortedlist]
    sortedlist.remove("city_id")
    sortedlist = ["city_id", *sortedlist]
    df = df.reindex(sortedlist, axis=1)
    return df
     
# Save DataFrame(s) in JSON-format
def save_to_file(df, file):
    df = df.to_json(orient="records", indent=4)

    if not os.path.exists(HARMONIZEDPATH + 'data_transformed.txt'):
            with open(HARMONIZEDPATH + 'data_transformed.txt', 'w') as fh:
                fh.write('')

    with open(HARMONIZEDPATH + 'data_transformed.txt', 'r') as fh:
        filelist = fh.read().split(',')
        if file not in filelist:
            with open(HARMONIZEDPATH+file, 'w') as f:
                json.dump(json.loads(df),f, indent=4)
            with open(HARMONIZEDPATH + 'data_transformed.txt', 'a') as f:
                f.write(file + ',')

# Find city_id in the city-log.txt 
def find_id_from_log_file(df, filename):
    with open(SQLPATH+'cities.txt','r') as fh:
        citydict = eval(fh.read())
        city_index = citydict["city"].index(re.findall(r'[a-öA-Ö]+', filename)[0])
        city_id = citydict["city_id"][city_index]
        df["city_id"] = city_id
    return df

    
def file_in_log_file(file):
    if not os.path.exists(HARMONIZEDPATH + 'data_transformed.txt'):
        with open(HARMONIZEDPATH + 'data_transformed.txt', 'w') as fh:
                fh.write('')
    with open(HARMONIZEDPATH+'data_transformed.txt','r') as fh:
        filelist = fh.read().split(',')
        if file in filelist:
            return False
        else:
            return True


def harmonize_data_files(RAWPATH=RAWPATH):
    os.chdir(RAWPATH)
    for file in glob.glob('*.json'):
        filepath = RAWPATH + file
        if file_in_log_file(file):
            with open(filepath,'r') as f:
                js = json.load(f)
        else:
            continue
        df = harmonize_dict(js)
        find_id_from_log_file(df,file)
        df = sort_columns(df)
        #df = convert_datetime(df)
        save_to_file(df,file)


if __name__ == '__main__':
    harmonize_data_files()

