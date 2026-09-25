import pandas as pd
import matplotlib.pyplot as plt

# Leser PVGIS-data
df = pd.read_csv(
    "power-system-data/load/pvgis.csv",
    skiprows=10
)

# Gjør tidskolonnen om til datetime
df["time"] = pd.to_datetime(
    df["time"],
    format="%Y%m%d:%H%M",
    errors="coerce"
)

# Fjerner ugyldige rader
df = df.dropna(subset=["time"])

# Velger én dag
dag = df[df["time"].dt.date == pd.to_datetime("2020-06-16").date()].copy()

# Lager tid i timer
dag["timer"] = dag["time"].dt.hour + dag["time"].dt.minute / 60

# Plotter bare PVGIS-data
plt.plot(dag["timer"], dag["G(i)"], label="PVGIS-data")

plt.xlabel("Tid [timer]")
plt.ylabel("Solinnstråling [W/m²]")
plt.title("PVGIS-data for 16. juni 2020")
plt.grid()
plt.legend()

plt.show()