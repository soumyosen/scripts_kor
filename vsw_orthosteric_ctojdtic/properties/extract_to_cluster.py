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


df = pd.read_csv("properties/mols_to_clusterize.csv")
list_of_names = df["NAMES"].tolist()

def extract_poses(names_in_bundle, filename):
      extracted_poses = []
      with structure.StructureReader(filename) as reader:
           for i, st in enumerate(reader):
               if st.title in names_in_bundle:
                   extracted_poses.append(st)
      return extracted_poses


if __name__ == "__main__":

      filename = sys.argv[1]
      #filename = "clustering_result.mae"
      extracted_ligands = extract_poses(list_of_names, filename)
      with structure.StructureWriter("ligs_to_clusterize.mae") as writer:
               for st in extracted_ligands:
                    print(st.title)
                    writer.append(st)
