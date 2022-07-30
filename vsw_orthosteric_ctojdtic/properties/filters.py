import sys
import time
import argparse
import pandas as pd
from rdkit import Chem
import multiprocessing as mp
from multiprocessing import Pool


# Filter function
mcf = pd.read_csv('mcf.csv')
pains = pd.read_csv('wehi_pains.csv', names=['smarts', 'names'])
smarts_list = [Chem.MolFromSmarts(x) for x in mcf.append(pains, sort=True)['smarts'].values]

def chemical_filters(smiles, allowed=None, smarts_filters=smarts_list):

    # Parse molecule
    mol = Chem.MolFromSmiles(smiles)

    if mol is None or smiles is None or len(smiles) == 0:
        return 'PARSEFAIL'

    # Check the number of atoms in aromatic moieties
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() != 0 and any(
            len(x) >= 8 for x in ring_info.AtomRings()):
        return 'RING8FAIL'

    # Check allowed atom types
    allowed = allowed or {'C', 'N', 'S', 'O', 'F', 'Cl', 'Br', 'H'}
    if any(atom.GetSymbol() not in allowed for atom in mol.GetAtoms()):
        return 'DISALLOWEDFAIL'

    # SMARTS filters
    h_mol = Chem.AddHs(mol)
    if any(h_mol.HasSubstructMatch(smarts) for smarts in smarts_filters):
        return 'MCFFAIL'

    return 1


df = pd.read_csv("for_next_phase_only_lig_smiles_frm_maestro_removed_props.txt")
num_input_rows = df.shape[0]
print(f"Input data dimensions: {df.shape}")

smiles_list = df['SMILES'].tolist()
filter_indexes = []

for i in range(num_input_rows):
    filter_index = chemical_filters(smiles_list[i])
    filter_indexes.append(filter_index)
    

df["FILTERS"] = filter_indexes

#print(df)
df.to_csv("for_next_phase_only_lig_smiles_frm_maestro_removed_props_filters.txt", index=False)

df1 = df[(df.FILTERS == 1)]
num_output_rows = df1.shape[0]
fraction_passed = "%.1f" % (num_output_rows / num_input_rows * 100.0)
print("%s of %s passed filters: %s" % (num_output_rows, num_input_rows, fraction_passed))

