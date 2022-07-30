#########How to use?
######### $SCHRODINGER/run ./take_out_mcule_available.py for_extract_available_molecules.maegz 

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


def get_ligs_info(filename):
      '''
      extracts the ligands' name and property
      '''
      get_list_available = []
      get_list_not_available = []
      with structure.StructureReader(filename) as reader:  
           for i, st in enumerate(reader):
               #print(st.property.keys())
               if st.property['s_user_vendor']=="mcule":
                   get_list_available.append(i)
               else:
                   get_list_not_available.append(i)
      twolists = [get_list_available, get_list_not_available]
      return twolists 


def extract_poses(indexlist_of_poses, filename, output_file):
      extracted_poses = []
      with structure.StructureReader(filename) as reader:
           for i, st in enumerate(reader):
               if i in indexlist_of_poses:
                   extracted_poses.append(st)
      #return extracted_poses
      with structure.StructureWriter(output_file) as writer:
               for st in extracted_poses:
                    print(st.title)
                    writer.append(st)


if __name__ == "__main__":
      filename = sys.argv[1]
      #filename = "clustering_result.mae"
      index_available, index_not_available = get_ligs_info(filename)
      print("Number of available molecules from mcule")
      print(len(index_available))
      print("Number of unavailable molecules from mcule")
      print(len(index_not_available))
      extract_poses(index_available, filename, "fp0.75_cluster_lowestE_charged_int_1_with_polar_int_find_mcule.mae")
      #extract_poses(index_not_available, filename, "fp0.75_cluster_lowestE_charged_int_0_with_polar_int_not_find_mcule.mae")

              





