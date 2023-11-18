import os
import wget
import zipfile
import pandas as pd
import shelve
import streamlit as st
data_storage_folder = os.path.join(os.getcwd(), "Data\Storage")
cacheZip = {}
cacheDF = {}

def CacheZip(key, zipFileUrl):
    if key in cacheZip:
        return cacheZip[key]    
    zip_file_path = os.path.join(data_storage_folder, key + ".zip")
    wget.download(zipFileUrl, out=zip_file_path)
    zf = zipfile.ZipFile(zip_file_path)
    cacheZip[key] = zf
    return cacheZip[key]

def csvURLtoDF(csvURL: str) ->pd.DataFrame:
    df = pd.read_csv((csvURL), sep = ";", low_memory=False)
    return df


def CacheDF(df, key):
    if key in cacheDF:
        return cacheDF[key]
    with shelve.open(os.path.join(data_storage_folder, "savedDictionary")) as d:
        d[key] = df
    cacheDF[key] = df

    return cacheDF[key]

def dumpDict(data, name):
    with shelve.open(os.path.join(data_storage_folder, "savedDictionary")) as d:
        d[name] = data

def checkKeyinDict(key):
    with shelve.open(os.path.join(data_storage_folder, "savedDictionary")) as d:
        return key in d

def loadDict(name):
    with shelve.open(os.path.join(data_storage_folder, "savedDictionary")) as d:
        if name not in d:
            return 0
        return d[name]
    

import streamlit as st
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @staticmethod
    def get(id, **kwargs):
        # Check if a unique SessionState object for the given id exists
        if not hasattr(st, '_global_session_states'):
            st._global_session_states = {}
        if id not in st._global_session_states:
            st._global_session_states[id] = SessionState(**kwargs)
        return st._global_session_states[id]

    

def delete_files():
    files_to_delete = [
        "savedDictionary.bak",
        "savedDictionary.dat",
        "savedDictionary.dir",
        "fldArea.zip"
    ]
    
    for file in files_to_delete:
        file_path = os.path.join(data_storage_folder, file)
        if os.path.exists(file_path):
            os.remove(file_path)

def clear_state(state:SessionState):
    state.result = []
    state.method = []
    state.precision = []
    state.field = []
def clear_state2(state:SessionState):
    state.result = []
    state.time_frame = []
    state.production_data = []
    state.field = []

    