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

print(df.columns)
print(df.head())

print("\nOppgave 8")
print(f"Maksimal produksjon: {df['Production'].max():.2f}")
print(f"Minimal produksjon: {df['Production'].min():.2f}")
print(f"Gjennomsnittlig produksjon: {df['Production'].mean():.2f}")

print("\nOppgave 9")
print(f"Maksimal nettoeffekt: {df['Netto'].max():.2f}")
print(f"Tidspunkt: {df['Netto'].idxmax()}")

print(f"Minimal nettoeffekt: {df['Netto'].min():.2f}")
print(f"Tidspunkt: {df['Netto'].idxmin()}")

print(f"\nTotal produksjon: {total_produksjon:.2f}")

df.plot(
    y=["Production", "Consumption", "Netto"],
    figsize=(10, 5)
)

plt.title("Produksjon, forbruk og nettoeffekt over tid")
plt.xlabel("Tid")
plt.ylabel("Effekt")
plt.grid(True)
plt.legend(["Produksjon", "Forbruk", "Nettoeffekt"])

plt.tight_layout()
plt.show()