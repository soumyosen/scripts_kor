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

#import MDAnalysis as mda
import numpy as np
import prolif
import pandas as pd
from rdkit.Chem import AllChem
from rdkit import Chem
import os

#files = os.listdir(path='.')
#print(len(files))

#extracted_poses = []
#with structure.StructureReader("for_next_phase_trial.maegz") as reader:
#    for i, st in enumerate(reader):
#        extracted_poses.append(st.title)
#        structure.write("%s.pdb" % st.title)
#
#print(extracted_poses)


#complex_files = []
#for each_file in files:
#    if each_file.endswith('.pdb'):
#        complex_files.append(each_file)
#print(len(complex_files))
##print(complex_files)
#
#AA_dic = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
#     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
#     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
#     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
#
#dic1 = {'HBAcceptor': 'HBDonor', 'HBDonor': 'HBAcceptor', 'Cationic': 'Anionic', 
#        'Anionic': 'Cationic', 'Hydrophobic': 'Hydrophobic', 'CationPi': 'PiCation', 
#        'PiCation': 'CationPi', 'PiStacking': 'PiStacking', 'FaceToFace': 'FaceToFace',
#        'EdgeToFace': 'EdgeToFace', 'BaseMetallic': 'BaseMetallic'}
#
#class HBAcceptor(prolif.interactions.HBAcceptor):
#   def __init__(self):
#       super().__init__(acceptor="[#7,#8,F,-{1-};!+{1-}]")
#
#class HBDonor(prolif.interactions.HBDonor):
#   def __init__(self):
#       super().__init__(acceptor="[#7,#8,F,-{1-};!+{1-}]")
#
#
#file_number = 1
#df = pd.DataFrame()
#
#for i in complex_files:
#    u1 = mda.Universe(i)
#    u1.atoms.guess_bonds(vdwradii={'Cl': 1.75, 'Br': 1.85, 'Mn': 2.45})
#    prot1 = u1.select_atoms("same residue as protein and around 10.0 (resname UNK)")
#    lig1 = u1.select_atoms("resname UNK")
#    #fp1 = prolif.Fingerprint(interactions="all")
#    #df1 = fp1.run(u1.trajectory[:], lig1, prot1).to_dataframe()
#    backbone = Chem.MolFromSmarts("[C^2](=O)-[C;X4](-[H])-[N;+0]-[H]")
#    backbone_pro = Chem.MolFromSmarts("[C](=O)-[C@](-[H])-[N-]")
#    prot1_mol = prolif.Molecule.from_mda(prot1)
#    prot1_mol = AllChem.DeleteSubstructs(prot1_mol, backbone)
#    prot1_mol = AllChem.DeleteSubstructs(prot1_mol, backbone_pro)
#    prot1_mol = prolif.Molecule(prot1_mol)
#    lig1_mol = prolif.Molecule.from_mda(lig1)
#    fp1 = prolif.Fingerprint(interactions="all")
#    data1 = fp1.generate(lig1_mol, prot1_mol)
#    data1["Frame"] = 0
#    ifp1 = [data1]
#    df1 = prolif.to_dataframe(ifp1, fp1.interactions.keys())
#
#
#    df2 = df1.unstack(level=-1).reset_index()
#    df3 = df2.drop("Frame", axis=1)
#    df3 = df3.rename(columns={0: "Present"})
#    #print(df3)
#    df3["Present"] = df3["Present"].astype(int)
#    df3["chain"] = df3["protein"].str.split('.').str[1]
#    df3["resname"]=df3["protein"].str[0:3]
#    df3["res_num"]=df3["protein"].str.split('.').str[0].str[3:]
#    df3["amino_acid"]=df3["resname"].map(AA_dic)
#    df3["amino_acid"]=df3["amino_acid"]+df3["res_num"]
#    df3["chain_aa"]=df3[['chain', 'amino_acid']].agg('_'.join, axis=1)
#    df3["interaction1"]=df3["interaction"].map(dic1)
#    print(df3)
#    df3["fp"]=df3[['chain_aa', 'interaction1']].agg('_'.join, axis=1)
#    df4 = df3.pivot(index=["ligand"], columns="fp", values="Present").reset_index()
#    #print(df4)
#    
#    lig_name = i.split("_")[1].split('.')[0]
#    df4["ligand"] = lig_name
#    df = pd.concat([df, df4], axis=0, join='outer')
#    df = df.fillna(0)
#    print("File number %s is done" % file_number)
#
#    #pd.options.display.float_format = '{:,.0f}'.format 
#    file_number = file_number+1
#    #df4.to_csv("%s.csv" % lig_name, index=False)
#
##df = df.apply(pd.to_numeric, errors='ignore')
#
#columns = df.columns.tolist()
#columns.remove("ligand")
#for elem in columns:
#    df[elem] = df[elem].apply(np.int64)
#
#df.to_csv("protSC_lig_int_FP_Hbond_def_change.csv", index=False)
#
