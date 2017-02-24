######### Set up Notebook Package parameters #########
print('Launching Notebook Package (NbPackage)...')
import sys
from os import environ
from os.path import join, realpath

DIR_PACKAGE = realpath('..')
environ['DIR_PACKAGE'] = DIR_PACKAGE
print('\tExported variable DIR_PACKAGE ({}).'.format(DIR_PACKAGE))

DIR_TOOLS = join(DIR_PACKAGE, 'tools/')
sys.path.insert(0, DIR_TOOLS)
print('\tExported variable DIR_TOOLS ({}), and added it to the path.'.format(DIR_TOOLS))

DIR_DATA = join(DIR_PACKAGE, 'data/')
print('\tExported variable DIR_DATA ({}).'.format(DIR_DATA))

DIR_RESULTS = join(DIR_PACKAGE, 'results/')
print('\tExported variable DIR_RESULTS ({}).'.format(DIR_RESULTS))

DIR_MEDIA = join(DIR_PACKAGE, 'media/')
print('\tExported variable DIR_MEDIA ({}).'.format(DIR_MEDIA))


######### Set up project-specific parameters #########
from pprint import pprint
import numpy as np
import pandas as pd