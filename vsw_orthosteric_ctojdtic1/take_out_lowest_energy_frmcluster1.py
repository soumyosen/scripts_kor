#########How to use?
######### $SCHRODINGER/run ./take_out_lowest_energy_frmcluster.py for_ext_lowE_9.0_fp0.75merge_cutoff.mae 

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
      get_list_cls = []
      with structure.StructureReader(filename) as reader:  
           for i, st in enumerate(reader):
               #print(st.property.keys())
               inf = [i, st.title, st.property['r_i_docking_score'], st.property['i_canvas_HClust::clusterHC\\_01::Cluster']] 
               get_list.append(inf)
               get_list_cls.append(st.property['i_canvas_HClust::clusterHC\\_01::Cluster'])
      get_list_cls = list(set(get_list_cls))
      twolists = [get_list_cls, get_list]
      return twolists 


def get_lowest_energy_pose(clslist, infolist):
      get_lowest_energy_list = []
      get_lowest_energy_index = []
      for i in clslist:
           lowest_score = 10.0
           for j in infolist:
                if j[3] == i:
                     if j[2] < lowest_score:
                          lowest_score = j[2]
                          lowest_score_pose = j
           
           get_lowest_energy_list.append(lowest_score_pose)
           get_lowest_energy_index.append(lowest_score_pose[0])
      twolists =[get_lowest_energy_index, get_lowest_energy_list]
      return twolists


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
      cls_of_ligs, info_of_ligs = get_ligs_info(filename)
      lowest_E_lig_index, lowest_E = get_lowest_energy_pose(cls_of_ligs, info_of_ligs)
      print(len(lowest_E_lig_index))
      print(lowest_E_lig_index)
      print(len(lowest_E))
      print(lowest_E)
      extracted_ligands = extract_poses(lowest_E_lig_index, filename)
      with structure.StructureWriter("fp0.75_cluster_lowE_9.0.mae") as writer:
               for st in extracted_ligands:
                    print(st.title)
                    writer.append(st)

              





