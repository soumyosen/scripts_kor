import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("output-report.csv", names=["Ligands", "ZINC_index", "Docking_score", "Hbond", "Metal", "vdW", "Coul"])
#df["log_Ligands"] = np.log10(df["Ligands"])

x_pt = 219860
y_pt = -6.0

plt.plot(df["Ligands"], df["Docking_score"])
plt.ylabel("Docking Score (kcal/mol)", fontsize=16)
plt.xlabel("Ligands_count", fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.axvline(x=x_pt, color="red", linestyle='--')
plt.text(70000, -3.0, "x=%s" % x_pt, color="red", fontsize=16)
plt.axhline(y=y_pt, color="green", linestyle='--')
plt.text(990000, -8.5, "y=%s" % y_pt, color="green", fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()
plt.savefig("dockinng_score_SP_0.6_bbrc.png")

