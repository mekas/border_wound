from configparser import ConfigParser
import pandas as pd
from lib import *

conf_path = "app.conf"
config = ConfigParser()
config.read(conf_path)
section = 'TEST'
dirpath = config[section]['Dir']
df = pd.read_csv(config[section]['Input'])
PARS = 'PARAMETER'
alpha = float(config[PARS]['alpha'])
beta = float(config[PARS]['beta'])
gamma = float(config[PARS]['gamma'])
blur_width = int(config[PARS]['gaussian_kernel_width'])
density = int(config[PARS]['density'])

run_active_contour(dirpath, df, alpha, beta, gamma, blur_width, density)
