"""CODE PYTHON PROJET ANALYSE DE DONNÉES
AUTEURS : Thomas BOTTALICO, Frédéric JALAGUIER, Lucie LE SAUX, Mathieu NIVEAU, Adrien RIVET
DATE : Soutenance du 5 Mai"""

import pandas as pd

# Chargement des fichiers
df_temp = pd.read_csv("data/temperature_worldbank_2019_2023.csv")
df_precip = pd.read_csv("data/precipitations_worldbank_2019_2023.csv")
df_canicule = pd.read_excel("data/canicule_FAO_2020_2023.xlsx")
df_secheresse = pd.read_csv("data/secheresse_EMDAT.csv")
df_vin = pd.read_csv("data/production_vin_OIV.csv")
df_biere = pd.read_csv("data/production_biere_statista.csv")
df_prix = pd.read_excel("data/prix_conso_OECD_Eurostat.xlsx")
df_superficie = pd.read_csv("data/superficies_FAOSTAT.csv")

# Uniformisation des noms de pays
for df in [df_temp, df_precip, df_canicule, df_secheresse, df_vin, df_biere, df_prix, df_superficie]:
    df['Pays'] = df['Pays'].str.strip().str.lower().str.title()

# Fusion sur "Pays"
df_total = df_temp.merge(df_precip, on="Pays")
df_total = df_total.merge(df_canicule, on="Pays")
df_total = df_total.merge(df_secheresse, on="Pays")
df_total = df_total.merge(df_vin, on="Pays")
df_total = df_total.merge(df_biere, on="Pays")
df_total = df_total.merge(df_prix, on="Pays")
df_total = df_total.merge(df_superficie, on="Pays")

# Nettoyage
df_total = df_total.fillna(method="ffill").round(2)

# Export
df_total.to_csv("climat_apero.csv", index=False, encoding="utf-8-sig")

print("Fichier final généré : climat_apero.csv")
