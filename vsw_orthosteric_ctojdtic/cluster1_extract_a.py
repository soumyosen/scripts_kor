#########How to use?
######### $SCHRODINGER/run ./cluster1_extract.py clustered.maegz


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
      extracts the ligands' name and docking scores
      '''

      get_list = []
      with structure.StructureReader(filename) as reader:
           for i, st in enumerate(reader):
              # print(st.property.keys())
               inf = [i, st.title, st.property['i_user_Label']]
               get_list.append(inf)
      return get_list

def get_goodmol(infolist):
      get_goodmol_index = []
      for j in infolist:
            if j[2] == 1:
                get_goodmol_index.append(j[0])
      return get_goodmol_index


def extract_poses(indexlist_of_poses, filename):
      extracted_poses = []
      with structure.StructureReader(filename) as reader:
           for i, st in enumerate(reader):
               if i in indexlist_of_poses:
                   extracted_poses.append(st)
      return extracted_poses



if __name__ == "__main__":

      filename = sys.argv[1]
      #filename = "clustering_result.mae"
      info_of_ligs = get_ligs_info(filename)
      index_of_good_mol = get_goodmol(info_of_ligs)
      print(len(index_of_good_mol))
      extracted_ligands = extract_poses(index_of_good_mol, filename)
      with structure.StructureWriter("cluster1.maegz") as writer:
               for st in extracted_ligands:
                    print(st.title)
                    writer.append(st)

