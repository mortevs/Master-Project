import os, pandas as pd, shelve, streamlit as st
data_storage_folder = os.path.join(os.getcwd(), 'Data', 'Storage')
cacheDF = {}

def csvURLtoDF(csvURL: str) ->pd.DataFrame:
    df = pd.read_csv(csvURL, sep=",", encoding='utf-8', low_memory=False)
    return df
def commaCSVURLtoDF(csvURL: str) ->pd.DataFrame:
    df = pd.read_csv(csvURL, sep=",", encoding='utf-8', low_memory=False)
    return df
def OLDcsvURLtoDF(csvURL: str) ->pd.DataFrame:
    df = pd.read_csv((csvURL), sep = ";", low_memory=False)
    return df

def CacheDF(df, key):
    if checkKeyinDict(key):
        return loadDict(key)
    else:
        dumpDict(df, key)

        return loadDict(key)
        
# def checkKeyCached(key): #this code did not work as intended as is outdated
#         if key in cacheDF:
#             return True
#         else:
#             return False
    
def dumpDict(data, name):
    with shelve.open(os.path.join(data_storage_folder, 'savedDictionary')) as d:
        d[name] = data

def checkKeyinDict(key):
    with shelve.open(os.path.join(data_storage_folder, 'savedDictionary')) as d:
        return key in d

def loadDict(key):
    with shelve.open(os.path.join(data_storage_folder, 'savedDictionary')) as d:
        if key not in d:
            st.warning('An error has accured')
        else:
            loaded_data = d[key]
            return loaded_data
    
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @staticmethod
    def get(id, **kwargs):
        if not hasattr(st, '_global_session_states'):
            st._global_session_states = {}
        if id not in st._global_session_states:
            st._global_session_states[id] = SessionState(**kwargs)
        return st._global_session_states[id]

    def delete(id):
        if hasattr(st, '_global_session_states') and id in st._global_session_states:
            del st._global_session_states[id]

    def append(id, key, value):
        if not hasattr(st, '_global_session_states'):
            st._global_session_states = {}
        session_state = st._global_session_states.get(id)
        current_list = getattr(session_state, key, [])
        current_list.append(value)     
        setattr(session_state, key, current_list)
    
    def store_one(id, key, value):
        if not hasattr(st, '_global_session_states'):
            st._global_session_states = {}
        session_state = st._global_session_states.get(id)
        current_list = []
        current_list.append(value)     
        setattr(session_state, key, current_list)


def delete_files():
    files_to_delete = [
        "savedDictionary.bak",
        "savedDictionary.dat",
        "savedDictionary.dir",
        "wlbPoint.zip",
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

    