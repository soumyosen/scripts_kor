import sys
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from esol import *


df = pd.read_csv("for_next_phase_only_lig_smiles_frm_maestro_removed.txt", sep=" ", names=["SMILES", "NAMES"])
print(f'Dataset dimensions: {df.shape}')
smiles_list = df['SMILES'].tolist()
names_list = df['NAMES'].tolist()
num = len(smiles_list)

# WLogP
#p = Pool(np)
wlogp2 = []
tpsab2 = []
logs2 = []

esol_calculator = ESOLCalculator()

for i in range(num):
    mol = Chem.MolFromSmiles(smiles_list[i])
    name = names_list[i]
    wlogp1 = Descriptors.MolLogP(mol)
    tpsab1 = Descriptors.TPSA(mol, includeSandP=True)
    logs1 = esol_calculator.calc_esol(mol)
    wlogp2.append(wlogp1)
    tpsab2.append(tpsab1)
    logs2.append(logs1)

df['WLogP'] = wlogp2
df['TPSAB'] = tpsab2
df['LogS'] = logs2

df.to_csv("for_next_phase_only_lig_smiles_frm_maestro_removed_props.txt", index=False)
