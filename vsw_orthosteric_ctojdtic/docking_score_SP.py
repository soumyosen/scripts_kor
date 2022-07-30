import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("output-report.csv", names=["Ligands", "ZINC_index", "Docking_score", "Hbond", "Metal", "vdW", "Coul"])
#df["log_Ligands"] = np.log10(df["Ligands"])
#print(df[df["Docking_score"]<=-5.2].count())

x_pt = 1022022
y_pt = -5.2

plt.plot(df["Ligands"], df["Docking_score"])
plt.ylabel("Docking Score (kcal/mol)", fontsize=16)
plt.xlabel("Ligands_count", fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.axline((10340000, -3.33), (1040000, -5.13), color="red", lw=2)
plt.axvline(x=x_pt, color="red", linestyle='--')
plt.text(1200000, 0.5, "x=%s" % x_pt, color="red", fontsize=16)
plt.axhline(y=y_pt, color="green", linestyle='--')
plt.text(2000000, -7.0, "y=%s" % y_pt, color="green", fontsize=16)
plt.tight_layout()
#plt.show()
plt.savefig("docking_score_SP.png")

