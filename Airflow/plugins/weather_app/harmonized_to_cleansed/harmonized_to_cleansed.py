import pandas as pd 
import os,glob
import json

ROOTPATH = os.path.dirname(os.path.dirname(__file__))
HARMONIZEDPATH = ROOTPATH + '/data/testing/harmonized/'
CLEANEDPATH = ROOTPATH + '/data/testing/cleaned/'

def save_to_file(df, file):
    df = df.to_json( orient="records", indent=4)
    if not os.path.exists(CLEANEDPATH + 'data_transformed.txt'):
            with open(CLEANEDPATH+'data_transformed.txt','w') as fh:
                fh.write('') #Nuvarande variant fungerar.
    with open(CLEANEDPATH+'data_transformed.txt', 'r') as fh:
        
        filelist = fh.read().split(',')  
    if file not in filelist:
        with open(CLEANEDPATH+file,'w') as f:
            json.dump(json.loads(df),f, indent=4)
        with open(CLEANEDPATH+'data_transformed.txt', 'a') as f:
            f.write(file + ',')

def file_not_in_log_file(file):
    if not os.path.exists(CLEANEDPATH + 'data_transformed.txt'):
        with open(CLEANEDPATH + 'data_transformed.txt','w') as f:
            f.write('')
        return True
    with open(CLEANEDPATH+'data_transformed.txt','r') as fh:
        filelist = fh.read().split(',')
        if file in filelist:
            return False
        else:
            return True

def data_file_cleaned():
    os.chdir(HARMONIZEDPATH)
    for file in glob.glob('*.json'):
        filepath = HARMONIZEDPATH + file
        if file_not_in_log_file(file):
            pass
        else:
            continue
        df = pd.read_json(filepath)
        save_to_file(df,file)
    print("Data Cleansed")

        
if __name__ == '__main__':
    data_file_cleaned()
