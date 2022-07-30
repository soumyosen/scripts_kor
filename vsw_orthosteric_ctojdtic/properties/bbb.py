import pandas as pd
import numpy as np
from matplotlib.patches import Ellipse

BOILED_EGG_BBB_ELLIPSE = Ellipse((38.117, 3.177), 82.061, 5.557, -0.171887)
def bbb_score(wlogp, tpsa):
    if BOILED_EGG_BBB_ELLIPSE.contains_point((tpsa, wlogp)):
        bbb = 1
    else:
        bbb = 0
    return bbb


df = pd.read_csv("for_next_phase_only_lig_smiles_frm_maestro_removed_props_filters.txt")
#df

df['BBB'] = df.apply(lambda x: bbb_score(x.WLogP, x.TPSAB), axis=1)
df.to_csv("final_props_filters_bbb.txt", index=False)


