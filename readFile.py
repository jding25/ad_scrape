from pandas import *
import re
import pickle
from random import sample
import csv

# write list to binary file
def write_list(list, filename):
    # store list in binary file so 'wb' mode
    with open(filename, 'wb') as fp:
        pickle.dump(list, fp)
        print('Done writing list into a binary file')

# Read list to memory
def read_list(list_name):
    # for reading also binary mode 
    with open(list_name, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

