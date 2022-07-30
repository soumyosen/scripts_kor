
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
 

with structure.StructureReader("to_cluster_binding_domain.maegz") as reader:
    mol_cent_x = []
    mol_cent_y = []
    mol_cent_z = []
    names = []
    for i, st in enumerate(reader):
        x_coord = []
        y_coord = []
        z_coord = []
        num = 0
        for atom in st.atom:
            atomic_number = atom.atomic_number
            if (atomic_number > 1):
                x_coord.append(atom.x)
                y_coord.append(atom.y)
                z_coord.append(atom.z)

        x_avg = np.average(x_coord)
        y_avg = np.average(y_coord)
        z_avg = np.average(z_coord)
 
        mol_cent_x.append(x_avg)
        mol_cent_y.append(y_avg)
        mol_cent_z.append(z_avg)
        names.append(st.title)


df = pd.DataFrame()
df["Name"] = names
df["X"] = mol_cent_x
df["Y"] = mol_cent_y
df["Z"] = mol_cent_z

print(df)
df.to_csv("lig_center_coord.csv", index=False)
