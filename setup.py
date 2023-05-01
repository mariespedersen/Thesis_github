import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import seaborn
import matplotlib.cm as cm
import requests
import json
import pandas as pd
import time
import datetime
import os
import math
import scipy.stats
from unidecode import unidecode
import sys
import glob
import re
import random
import pickle
import copy
import nltk
import itertools
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import Image
import collections
import warnings
warnings.filterwarnings('ignore')
from bs4 import BeautifulSoup
import wikipedia
from tqdm import tqdm

# Similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

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
