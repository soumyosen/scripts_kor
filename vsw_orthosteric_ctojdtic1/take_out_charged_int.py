#########How to use?
######### $SCHRODINGER/run ./take_out_charged_int.py for_extract_charged_int_with_polar_int.maegz 

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
      get_list_charged_int_1 = []
      get_list_charged_int_0 = []
      with structure.StructureReader(filename) as reader:  
           for i, st in enumerate(reader):
               #print(st.property.keys())
               if st.property['i_u_charged\\_int']==1:
                   get_list_charged_int_1.append(i)
               else:
                   get_list_charged_int_0.append(i)
      twolists = [get_list_charged_int_1, get_list_charged_int_0]
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
      index_charged_int_1, index_charged_int_0 = get_ligs_info(filename)
      print("Number of molecules with charged interaction")
      print(len(index_charged_int_1))
      print("Number of molecules with no D138 interaction")
      print(len(index_charged_int_0))
      extract_poses(index_charged_int_1, filename, "fp0.75_cluster_lowestE_charged_int_1_with_polar_int.mae")
      extract_poses(index_charged_int_0, filename, "fp0.75_cluster_lowestE_charged_int_0_with_polar_int.mae")

              





