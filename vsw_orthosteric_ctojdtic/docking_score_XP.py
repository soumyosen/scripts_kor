import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("output-report_XP.csv", names=["Ligands", "ZINC_index", "Docking_score", "Hbond", "Metal", "vdW", "Coul"])
#df["log_Ligands"] = np.log10(df["Ligands"])
#print(df[df["Docking_score"]<=-5.2].count())

x_pt = 8150
y_pt = -8.0

plt.plot(df["Ligands"], df["Docking_score"])
plt.ylabel("Docking Score (kcal/mol)", fontsize=16)
plt.xlabel("Ligands_count", fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
#plt.axline((914000, -4.0), (100000, -6.5), color="red", lw=2)
plt.axvline(x=x_pt, color="red", linestyle='--')
plt.text(140000, -2.0, "x=%s" % x_pt, color="red", fontsize=16)
plt.axhline(y=y_pt, color="green", linestyle='--')
plt.text(140000, -9.0, "y=%s" % y_pt, color="green", fontsize=16)
plt.tight_layout()
plt.show()
#plt.savefig("docking_score_XP.png")

