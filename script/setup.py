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
import math
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

# my packages
import preprocessing as pre
import query as q

from plotly.subplots import make_subplots
from IPython.display import Image
from bs4 import BeautifulSoup
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
from unidecode import unidecode
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from collections import Counter
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