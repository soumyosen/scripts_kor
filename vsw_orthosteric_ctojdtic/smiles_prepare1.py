import os
import sys
import argparse
import warnings
import numpy as np

from schrodinger import structure
from schrodinger.structutils import analyze
from schrodinger.structutils.analyze import generate_smiles
from schrodinger import adapter

from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

myfile = open("for_next_phase_only_lig_smiles1.txt", 'w')

with structure.StructureReader("for_next_phase_only_lig-out.maegz") as reader:
    for i, st in enumerate(reader):
        name = st.title
        smi = analyze.generate_smiles(st)
        myfile.write("%s,%s\n" % (name,smi))


myfile.close()


