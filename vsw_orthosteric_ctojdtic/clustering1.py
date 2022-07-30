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
from scipy.spatial import distance as ssd

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
                    if tc < args.cutoff:
                        btc = True
                        return False
    if btc:
        return False
    else:
        return True
                        
# Parse command line
parser = argparse.ArgumentParser()
parser.add_argument('--datafile', help='Mestro file with SMILES column', type=str)
parser.add_argument('--cutoff', help='Cutoff for inter-cluster Tanimoto scores', type=float, default=0.7)
parser.add_argument('--draw', help='Draw molecules with lowest docking score from each cluster', action='store_false')
parser.add_argument('--output', help='Prefix for output files')
args = parser.parse_args()

# Read mae file and calculate fingerprints
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
        tc = DataStructs.TanimotoSimilarity(fpsj, fpsi)
        hmap[i, j] = tc

hmap1 = 1 - hmap
hmap1_array = ssd.squareform(hmap1) 
# Clustering
linked = linkage(hmap1_array, 'single')

# Cluster assignments with inter-cluster tc >= 0.7
nclusters = 2
final_nclusters = False
while final_nclusters == False:
    clusters = assign_clusters(linked, nclusters)
    final_nclusters = tc_intercluster(clusters, cutoff=args.cutoff)    
    if final_nclusters == False:
        nclusters += 1         
print(f'The final number of clusters is {nclusters}')

# Find cluster member with lowest docking score
hsts = []
hsmi = []
hmol = []
httl = []
hscr = []
hlgd = []
for cluster in clusters:
    hs = 999999.
    if len(cluster) > 1:
        for i in cluster:
            score = score_list[i]
            if score < hs:
                hs = score
                hm = i
        hsts.append(st_list[hm])
        hsmi.append(smi_list[hm])
        hmol.append(mol_list[hm])
        httl.append(ttl_list[hm])
        hscr.append(hs)
        legend = format(hs, '.2f')
        hlgd.append(ttl_list[hm] + ": " + legend)
    else:
        hsts.append(st_list[cluster[0]])      
        hsmi.append(smi_list[cluster[0]])
        hmol.append(mol_list[cluster[0]])
        httl.append(ttl_list[cluster[0]])
        hscr.append(score_list[cluster[0]])
        legend = format(score_list[cluster[0]], '.2')
        hlgd.append(ttl_list[cluster[0]] + ": " + legend)

# Sort lists by docking score
indices = sorted(range(len(hscr)), key=hscr.__getitem__)
hscr = sorted(hscr)
hsts = [hsts[i] for i in indices]
hsmi = [hsmi[i] for i in indices]
hmol = [hmol[i] for i in indices]
httl = [httl[i] for i in indices]
hlgd = [hlgd[i] for i in indices]

# Save molecules with best docking score from each cluster
with structure.StructureWriter(args.output + '.mae') as writer:
    for i, st in enumerate(hsts):
        writer.append(st)
        print(f'cluster: {i} --> {st.title}: doking score = {hscr[i]}')
 
# Draw molecules with best docking scores from each cluster
if args.draw:
    img = Draw.MolsToGridImage(hmol, molsPerRow=6, legends=hlgd)
    img.save(args.output + '.png')
