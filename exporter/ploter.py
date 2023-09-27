"""Simple script for plotting the contents of results.csv."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.figure(dpi=500)

df = pd.read_csv("results.csv")

x = df["rule_hits_records"]
y = df["memory_consumption"] / 1e6

m, b = np.polyfit(x, y, 1)

plt.plot(x, y, "yo")
plt.plot(x, m * x + b, "--k", label=f"{m*1e6:.2f}GB * (million of records) + {b:.2f}GB")

plt.xlabel("# Rule Hits records")
plt.ylabel("Memory usage (GB)")
plt.ylim(ymin=0)

plt.legend()
plt.grid(axis="x", color="0.95")

plt.savefig("results.jpg")
