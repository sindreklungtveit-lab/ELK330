import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

##sjekker fil
#df = pd.read_csv("power-system-data/load/forbruk_2025.csv")

#print(df.columns)
#print(df.head())

df = pd.read_csv("power-system-data/load/forbruk_2025.csv")

#gir mer forståelig navn en Unnamed til tidsvariabel
df = df.rename(columns={"Unnamed: 0": "timestamp"})

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

df["måned"] = df["timestamp"].dt.month

# Beregn gjennomsnitt
maanedlig_snitt = df.groupby("måned")["Actual Load"].mean()

maaneder = [
    "Januar", "Februar", "Mars", "April",
    "Mai", "Juni", "Juli", "August",
    "September", "Oktober", "November", "Desember"
]

# Lag en ny tabell
resultat = pd.DataFrame({
    "Måned": maaneder,
    "Gjennomsnittlig last (MW)": maanedlig_snitt.values
})

print(resultat.to_string(index=False))

resultat.to_csv("power-system-data/results/manedlig_last_2025.csv", index=False)

#Lag figur
plt.figure(figsize=(10, 5))

plt.plot(
    resultat["Måned"],
    resultat["Gjennomsnittlig last (MW)"],
    marker="o"
)

#plott detaljer
plt.title("Gjennomsnittlig last per måned i 2025")
plt.xlabel("Måned")
plt.ylabel("Gjennomsnittlig last (MW)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

output_file = Path(__file__).parent.parent / "results" / "manedlig_last_2025.png"
#lagre og vis figur
plt.savefig(output_file)
plt.show()


#Beregn statistikk for hver måned
statistikk = df.groupby("måned")["Actual Load"].agg(
    Høyeste="max",
    Laveste="min",
    Standardavvik="std"
)

#månedsnavn
maaneder = [
    "Januar", "Februar", "Mars", "April",
    "Mai", "Juni", "Juli", "August",
    "September", "Oktober", "November", "Desember"
]

statistikk.index = maaneder
statistikk.index.name = "Måned"

#print statistikk
print(statistikk)

# Lagre som CSV fil
output_file = (
    Path(__file__).parent.parent
    / "results"
    / "manedlig_last_statistikk_2025.csv"
)

statistikk.to_csv(output_file)