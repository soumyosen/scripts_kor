import sys
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
import multiprocessing as mp
from multiprocessing import Pool
from esol import *


def calc_wlogp(smiles):
    mol = Chem.MolFromSmiles(smiles)
    wlogp = Descriptors.MolLogP(mol)
    return wlogp

def calc_tpsab(smiles):
    mol = Chem.MolFromSmiles(smiles)
    tpsab = Descriptors.TPSA(mol, includeSandP=True)
    return tpsab

def calc_logs(smiles):
    mol = Chem.MolFromSmiles(smiles)
    esol_calculator = ESOLCalculator()
    logs = esol_calculator.calc_esol(mol)
    return logs


# Set up calculation
np = mp.cpu_count()
p = Pool(np)

df = pd.read_csv("for_next_phase_only_lig_smiles_frm_maestro.txt", sep=" ", names=["SMILES", "NAMES"])
print(f'Dataset dimensions: {df.shape}')
smiles_list = df['SMILES'].tolist()

# WLogP
p = Pool(np)
wlogp = list(p.map(calc_wlogp, smiles_list))
df['WLogP'] = wlogp

# TPSAB adapted from https://github.com/bfmilne/pyBOILEDegg/blob/main/pyBOILEDegg.py
p = Pool(np)
tpsab = list(p.map(calc_tpsab, smiles_list))
df['TPSAB'] = tpsab

# LogS adapted from https://github.com/PatWalters/solubility
p = Pool(np)
logs = list(p.map(calc_logs, smiles_list))
df['LogS'] = logs
