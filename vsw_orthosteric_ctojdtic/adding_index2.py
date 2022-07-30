import os
import warnings
import sys, getopt
import subprocess
import re
import pandas as pd
import numpy as np

from schrodinger import structure
from schrodinger.structutils import analyze
from schrodinger.structutils.analyze import generate_smiles
from schrodinger import adapter

allstr = []
with structure.StructureReader("for_next_phase_only_lig_out_4removed.maegz") as reader:
     for i, st in enumerate(reader):
          i1 = str(i)
          mol_name = "mol_" + i1
          st.property['s_u_uname'] = mol_name
          allstr.append(st)


with structure.StructureWriter("for_next_phase_only_lig_out_4removed_with_ind2.maegz") as writer:
           for st in allstr:
              writer.append(st)
