import pandas as pd
import numpy as np
from datetime import datetime
import json

with open('./data/temp/test_data/nifty50.json') as f:
    data = json.load(f)

