#########How to use?
######### $SCHRODINGER/run ./list_of_ligs.py fp0.75_cluster_lowestE_charged_int_1_with_polar_int.mae 

import os
import warnings
import sys, getopt
import subprocess
import re
import pandas as pd
import numpy as np
import re

from schrodinger import structure
from schrodinger.structutils import analyze
from schrodinger.structutils.analyze import generate_smiles
from schrodinger import adapter

filename = sys.argv[1]
lig_name = []

with structure.StructureReader(filename) as reader:
    for i, st in enumerate(reader):
        lig_name.append(st.title)



def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

lig_name.sort(key=natural_keys)

print(lig_name)
s = " "
lig_name1 = s.join(lig_name)
print(lig_name1)
