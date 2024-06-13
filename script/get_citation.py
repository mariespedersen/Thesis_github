# importing os module
import seaborn
import requests
import json
import time
import datetime
import os
import math
import scipy.stats
import sys
import glob
import re
import random
import pickle
import copy
import nltk
import itertools
import collections
import wikipedia
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.cm as cm
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import warnings
warnings.filterwarnings('ignore')

from plotly.subplots import make_subplots
from IPython.display import Image
from bs4 import BeautifulSoup
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
from unidecode import unidecode
from matplotlib.ticker import FuncFormatter
from datetime import datetime 

# Similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# This should only be 'y' if the preprocessing.ipynb should be runned.
# ChangeFolder = input("Do you want to change the folder? (y/n) ")
ChangeFolder = 'n'
if ChangeFolder == "y":
    
    # check if a folder exists
    filepaths = ["G:/My Drive/Thesis/Data", "G:\Mit drev\Thesis\Data"]
    try:
        os.chdir(filepaths[0])
        i = 0
    except FileNotFoundError:
        try:
            os.chdir(filepaths[1])
            i = 1
        except:
            print("No valid filepath found")

    filepath = filepaths[i]

# Path to save figures in my dropbox folder
image_path = r'C:\Users\verga\Dropbox\Apps\Overleaf\Thesis\Pictures\\'


def main():

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Loading of data, time:", current_time)
    
    # load data
    df_invited = pd.read_csv('Data/factInvited.csv')
    df_proceedings = pd.read_csv('Data/factProceedings.csv')

    df = pd.concat([df_invited, df_proceedings], ignore_index=True)
    pd.set_option('display.max_rows', 15)

    full_name = df['Full name'].unique()

    ids = []
    orcids = []
    works_count = []
    results = []
    
    BASE_URL = 'https://api.openalex.org/'
    ENDPOINT = 'authors'
    MAIL = 'elsa@itu.dk'

    current_time = (datetime.now()).strftime("%H:%M:%S")
    print("Start author data retreival, time:", current_time)

    for i in full_name:

        filter = f'?search={i}'
        mail = f'&mailto={MAIL}'
        complete_url = BASE_URL + ENDPOINT + filter + mail
        response_json = requests.get(complete_url).json()
        author_data = response_json['results']

        results.append(len(author_data))

        # no results found
        if len(author_data) == 0:

            works_count.append([None])
            ids.append([None])
            orcids.append([None])

        # found only one results
        if len(author_data) == 1:

            works_count.append([author_data[0]['works_count']])
            ids.append([author_data[0]['id']])
            orcids.append([author_data[0]['orcid']])

        # found more results
        else:
            
            # store a list with the works count for every result
            works_count.append([author_data[result]['works_count'] for result in range(len(author_data))])
            # store a list with the ids for every result
            ids.append([author_data[result]['id'] for result in range(len(author_data))])
            # check on the orcid codes
            orcid_codes = [author_data[result]['orcid'] for result in range(len(author_data))]
            different_orcids = set(code for code in orcid_codes if code is not None)
            # manually adding a None value if no orcid code is found
            if not different_orcids:
                different_orcids.add(None)

            orcids.append(list(different_orcids))
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Finish author data retreival\nStrating building dataframe, time:", current_time)

    df_author_id = pd.DataFrame(columns = ['Full name', 'OpenAlex ID', 'ORCID', 'Works count'])
    df_author_id['Full name'] = full_name
    df_author_id['OpenAlex ID'] = ids
    df_author_id['ORCID'] = orcids
    df_author_id['Works count'] = works_count

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("FInish biulding dataframe\nStart saving data, time:", current_time)

    filename = "authorID.csv" # or factProceedings.csv
    filepath = "./Data/"
    df_author_id.to_csv(os.path.join(filepath, filename), index=False)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("The file is now saved, time:", current_time)

if __name__ == '__main__':
    main()