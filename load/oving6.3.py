import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leser PVGIS-data
df = pd.read_csv(
    "power-system-data/load/pvgis.csv",
    skiprows=10
)

df["time"] = pd.to_datetime(
    df["time"],
    format="%Y%m%d:%H%M",
    errors="coerce"
)

df = df.dropna(subset=["time"])
# Velg én dag, for eksempel 6. juni 2020
dag = df[df["time"].dt.date == pd.to_datetime("2020-06-16").date()].copy()

# Lager tid i timer
dag["timer"] = (
    dag["time"].dt.hour
    + dag["time"].dt.minute / 60
)

# Gauss-modell
t = np.linspace(0, 24, 500)

A = 950
mu = 12
sigma = 4

G = A * np.exp(
    -(t - mu)**2 / (2 * sigma**2)
)

# Plotter begge i samme figur
plt.plot(t, G, label="Gauss-modell")

plt.plot(
    dag["timer"],
    dag["G(i)"],
    label="PVGIS-data"
)

plt.xlabel("Tid [timer]")
plt.ylabel("Solinnstråling [W/m²]")
plt.title("Gauss-modell sammenlignet med PVGIS-data")
plt.grid()
plt.legend()

plt.show()