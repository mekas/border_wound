from configparser import ConfigParser
import pandas as pd
from lib import *

conf_path = "app.conf"
config = ConfigParser()
config.read(conf_path)
section='TEST'
dirpath = config[section]['Dir']
df = pd.read_csv(config[section]['Input'])
# print(df)
run_active_contour(dirpath, df)
