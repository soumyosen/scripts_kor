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


with structure.StructureReader(args.datafile) as reader:
   st_list = []
   smi_list = []
   mol_list = []
   fps_list = []
   ttl_list = []
   score_list = []
   for i, st in enumerate(reader):
       try:
           smi = analyze.generate_smiles(st)
           mol = Chem.MolFromSmiles(smi)
           fps = Chem.RDKFingerprint(mol)
           ttl = st.title
           score = st.property['r_i_docking_score']
           st_list.append(st)
           smi_list.append(smi)
           mol_list.append(mol)
           fps_list.append(fps)
           ttl_list.append(ttl)
           score_list.append(score)
       except:
           warnings.warn(f'Could not calculate fingerprints for {st.title} {smi}')

   nfps = len(fps_list)
   print(f'{nfps} fingerprints calculated')


# Calculate the pairwise similarities and store in "distance" matrix
hmap = np.empty(shape=(nfps, nfps))

for i,fpsi in enumerate(fps_list):
    for j,fpsj in enumerate(fps_list):
        tc = DataStructs.TanimotoSimilarity(fpsi, fpsj)
        hmap[i, j] = tc


