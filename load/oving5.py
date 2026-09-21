import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from scipy.optimize import curve_fit

mappe = Path(__file__).parent

filnavn = mappe / "consumption_per_group_mba_hour-all-no-0000-00-00.csv"

df = pd.read_csv(
    filnavn,
    sep=";",
    decimal=","
)


def belastning(t, L0, A, mu, sigma):
    L = np.full_like(t, L0, dtype=float)

    for Ai, mui, sigmai in zip(A, mu, sigma):
        L += Ai * np.exp(-(t - mui)**2 / (2 * sigmai**2))

    return L
df["STARTTID"] = (
    pd.to_datetime(df["STARTTID"], utc=True)
    .dt.tz_convert("Europe/Oslo")
)

df["SLUTTID"] = (
    pd.to_datetime(df["SLUTTID"], utc=True)
    .dt.tz_convert("Europe/Oslo")
)


# --------------------------------------------------
# Velger døgnprofil
# --------------------------------------------------

dato = "2026-09-15"

dogn = df[
    (df["STARTTID"].dt.date == pd.to_datetime(dato).date()) &
    (df["FORBRUKSGRUPPE"] == "Husholdning") &
    (df["PRISOMRÅDE"] == "NO2")
].copy()


dogn["time"] = dogn["STARTTID"].dt.hour

t = dogn["time"].to_numpy()
L_data = dogn["VOLUM_KWH"].to_numpy()


# --------------------------------------------------
# Modell
# --------------------------------------------------

def modell(t,
           L0,
           A1, mu1, sigma1,
           A2, mu2, sigma2,
           A3, mu3, sigma3):

    return (
        L0
        + A1 * np.exp(-(t - mu1)**2 / (2 * sigma1**2))
        + A2 * np.exp(-(t - mu2)**2 / (2 * sigma2**2))
        + A3 * np.exp(-(t - mu3)**2 / (2 * sigma3**2))
    )


# --------------------------------------------------
# Startverdier
# --------------------------------------------------

L_min = L_data.min()
L_spenn = L_data.max() - L_data.min()

p0 = [
    L_min,

    0.2 * L_spenn, 3, 3,
    0.5 * L_spenn, 8, 2,
    0.7 * L_spenn, 18, 3
]


# --------------------------------------------------
# Tilpasser modellen
# --------------------------------------------------

parametre, kovarians = curve_fit(
    modell,
    t,
    L_data,
    p0=p0,
    maxfev=100000
)


# --------------------------------------------------
# Resultater
# --------------------------------------------------

(
    L0,
    A1, mu1, sigma1,
    A2, mu2, sigma2,
    A3, mu3, sigma3
) = parametre


print(f"L0 = {L0:.2f}")

print(f"Natt:   A = {A1:.2f}, mu = {mu1:.2f}, sigma = {sigma1:.2f}")
print(f"Morgen: A = {A2:.2f}, mu = {mu2:.2f}, sigma = {sigma2:.2f}")
print(f"Kveld:  A = {A3:.2f}, mu = {mu3:.2f}, sigma = {sigma3:.2f}")


# --------------------------------------------------
# Plot
# --------------------------------------------------

# Lager glatt tidsakse til modellen
t_glatt = np.linspace(0, 23, 500)

# Beregner modellverdiene
L_fit = modell(t_glatt, *parametre)


# --------------------------------------------------
# PLOTT 1: Observerte data
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    t,
    L_data,
    "o-",
    label="Elhub-data"
)

plt.xlabel("Tid [h]")
plt.ylabel("Forbruk [kWh]")
plt.title("Observerte data - Husholdning NO2, 01.01.2021")

plt.xticks(range(0, 24, 2))
plt.grid()
plt.legend()

plt.show()


# --------------------------------------------------
# PLOTT 2: Modellert kurve
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    t_glatt,
    L_fit,
    label="Modellert kurve"
)

plt.xlabel("Tid [h]")
plt.ylabel("Forbruk [kWh]")
plt.title("Modellert døgnprofil")

plt.xticks(range(0, 24, 2))
plt.grid()
plt.legend()

plt.show()


# --------------------------------------------------
# PLOTT 3: Observerte data + modell
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    t,
    L_data,
    "o",
    label="Elhub-data"
)

plt.plot(
    t_glatt,
    L_fit,
    label="Modellert kurve"
)

plt.xlabel("Tid [h]")
plt.ylabel("Forbruk [kWh]")
plt.title("Observerte data og modellert døgnprofil")

plt.xticks(range(0, 24, 2))
plt.grid()
plt.legend()

plt.show()

print("\nParameterverdier:")
print(f"L0 = {L0:.2f}")

print(f"A1 = {A1:.2f}")
print(f"mu1 = {mu1:.2f}")
print(f"sigma1 = {sigma1:.2f}")

print(f"A2 = {A2:.2f}")
print(f"mu2 = {mu2:.2f}")
print(f"sigma2 = {sigma2:.2f}")

print(f"A3 = {A3:.2f}")
print(f"mu3 = {mu3:.2f}")
print(f"sigma3 = {sigma3:.2f}")