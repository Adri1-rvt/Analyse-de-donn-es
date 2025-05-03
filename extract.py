"""CODE PYTHON PROJET ANALYSE DE DONNÉES
AUTEURS : Thomas BOTTALICO, Frédéric JALAGUIER, Lucie LE SAUX, Mathieu NIVEAU, Adrien RIVET
DATE : Soutenance du 5 Mai"""

import pandas as pd
import requests
from io import StringIO

# 1. Température et précipitations - Our World in Data (OWID)
def get_owid_climate_data():
    url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Climate%20change%20-%20OWID%20based%20on%20Berkeley%20Earth/Climate%20change%20-%20OWID%20based%20on%20Berkeley%20Earth.csv"
    response = requests.get(url)
    df = pd.read_csv(StringIO(response.text))
    df = df[['country', 'year', 'average_temperature']].rename(columns={
        'country': 'Pays',
        'year': 'Année',
        'average_temperature': 'Température (°C)'
    })
    df = df[df['Année'] >= 2019]
    return df.groupby("Pays").mean(numeric_only=True).reset_index()

# 2. Superficie de vigne - FAOSTAT (extrait par code de domaine "QC" et élément "Area harvested")
def get_fao_vine_area_data():
    fao_api_url = (
        "https://fenixservices.fao.org/faostat/api/v1/en/data/QC"
        "?item_code=560&element_code=511&year=2022&format=csv"
    )
    response = requests.get(fao_api_url)
    df = pd.read_csv(StringIO(response.text))
    df = df.rename(columns={
        'Area': 'Pays',
        'Value': 'Superficie Vigne (ha)'
    })[['Pays', 'Superficie Vigne (ha)']]
    return df

# 3. Fusion et affichage
if __name__ == "__main__":
    df_temp = get_owid_climate_data()
    df_vigne = get_fao_vine_area_data()

    df_temp['Pays'] = df_temp['Pays'].str.strip().str.title()
    df_vigne['Pays'] = df_vigne['Pays'].str.strip().str.title()

    df_fusion = pd.merge(df_temp, df_vigne, on="Pays", how="inner")
    df_fusion.to_csv("donnees_auto_climat_vigne.csv", index=False, encoding="utf-8-sig")
    print("Fichier généré : donnees_auto_climat_vigne.csv")