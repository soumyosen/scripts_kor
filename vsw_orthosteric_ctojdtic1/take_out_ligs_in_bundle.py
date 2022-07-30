#########How to use?
######### $SCHRODINGER/run ./take_out_ligs_in_bundle.py fp0.7_cluster_lowE_9.0.mae

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


def get_ligs_info(filename, name_list):
      '''
      extracts the ligands' name and docking scores
      '''
      get_list_name = []
      with structure.StructureReader(filename) as reader:  
           for i, st in enumerate(reader):
               #print(st.property.keys())
               get_list_name.append(st.title)
      get_list_name = list(set(get_list_name))

      in_bundle = []
      for k in get_list_name:
          if k not in name_list:
              in_bundle.append(k)
      return in_bundle 


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
      ligs_not_in_bundle = ['ZINC000012603718', 'ZINC000040074723', 'ZINC000192211539', 'ZINC000009441025', 'ZINC000003384457', 
              'ZINC000019766489', 'ZINC000257316572', 'ZINC000003399286', 'ZINC000408710242', 'ZINC000023311197', 'ZINC000096097315', 
              'ZINC000224279473', 'ZINC000045789171', 'ZINC000225297448', 'ZINC000101796995', 'ZINC000034667289', 'ZINC000257305510', 
              'ZINC000223662051', 'ZINC000033585375', 'ZINC000006588340', 'ZINC000037246034', 'ZINC000583649723', 'ZINC000055254201', 
              'ZINC000033284191', 'ZINC000225558193', 'ZINC000012297376', 'ZINC000038756763', 'ZINC000009708833', 'ZINC000064566020', 
              'ZINC000096403049', 'ZINC000020207549', 'ZINC000091603908']
      ligs_in_bundle = get_ligs_info(filename, ligs_not_in_bundle)
      extracted_ligands = extract_poses(ligs_in_bundle, filename)
      with structure.StructureWriter("ligs_in_bundle_9.0.mae") as writer:
               for st in extracted_ligands:
                    print(st.title)
                    writer.append(st)

              





