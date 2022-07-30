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

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# Function definitions
def assign_clusters(linked_matrix, num_clusters):
    assignments = fcluster(linked_matrix, t=num_clusters, criterion='maxclust')
    clusters = [[] for x in range(num_clusters)]
    for i,cc in enumerate(assignments):
        clusters[cc-1].append(i)
    return clusters


def tc_intercluster(clust_list, cutoff=0.7):
    btc = False
    for cluster in clust_list:
        if len(cluster) > 1:
            for i in cluster:
                for j in cluster:
                    tc = hmap[i, j]
                    if tc < 0.7:
                        btc = True
                        #return False
    if btc:
        return False
    else:
        return True



# Read mae file and calculate fingerprints
with structure.StructureReader("cluster1_1st10.maegz") as reader:
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
        tc = DataStructs.TanimotoSimilarity(fpsj, fpsi)
        hmap[i, j] = tc

# Clustering
linked = linkage(hmap, 'single')

#clusters1 = [[] for x in range(5)]
#print(clusters1)

#nclusters = 5
#assignments1 = fcluster(linked, t=nclusters, criterion='maxclust')
#clusters = assign_clusters(linked, nclusters)
#print(clusters)
#print(assignments1)


# Cluster assignments with inter-cluster tc >= 0.7
nclusters = 2
final_nclusters = False
while final_nclusters == False:
    clusters = assign_clusters(linked, nclusters)
    final_nclusters = tc_intercluster(clusters, cutoff=0.7)
    print(final_nclusters)
    if final_nclusters == False:
        nclusters += 1
print(f'The final number of clusters is {nclusters}')


