
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#sjekker fil
df = pd.read_csv("power-system-data/load/load_data.csv",decimal=",")

df["Time(Local)"] = pd.to_datetime(
    df["Time(Local)"],
    dayfirst=True,utc=True)

df = df.set_index("Time(Local)")
df["Netto"] = df["Production"] - df["Consumption"]

maks_netto = df["Netto"].max()
min_netto = df["Netto"].min()

tid_maks_netto = df["Netto"].idxmax()
tid_min_netto = df["Netto"].idxmin()

total_produksjon = df["Production"].sum()


dogn = df.loc["2026-01-01 00:00":"2026-01-01 23:00"]

plt.plot(dogn.index, dogn["Consumption"])

plt.xlabel("Tid")
plt.ylabel("Forbruk")
plt.title("Lastprofil for 1. januar 2026")

plt.xticks(rotation=45)
plt.grid()

plt.tight_layout()
plt.show()