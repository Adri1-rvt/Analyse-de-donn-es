"""CODE PYTHON PROJET ANALYSE DE DONNÉES
AUTEURS : Thomas BOTTALICO, Frédéric JALAGUIER, Lucie LE SAUX, Mathieu NIVEAU, Adrien RIVET
DATE : Soutenance du 5 Mai"""

"""IMPORT DES LIBRAIRIES NÉCESSAIRES POUR L'ANALYSE"""
import pandas as pd                     # Pour manipuler les données tabulaires
import numpy as np                      # Pour les opérations numériques (non utilisé ici mais souvent utile)
import matplotlib.pyplot as plt         # Pour faire des graphiques
import seaborn as sns                   # Pour des visualisations statistiques plus jolies
from sklearn.preprocessing import StandardScaler  # Pour normaliser les données avant ACP
from sklearn.decomposition import PCA             # Pour effectuer l’analyse en composantes principales
from scipy import stats                           # Pour faire des tests statistiques
import matplotlib

"""CONFIGURATION DU BACKEND POUR L’AFFICHAGE DES GRAPHIQUES"""
# Ce backend permet d’éviter un bug d’affichage sur certaines machines, notamment pour moi sous Windows avec Tkinter
matplotlib.use('TkAgg')

"""CHARGEMENT ET PRÉPARATION DES DONNÉES"""
# On charge notre fichier CSV contenant les données récoltées
df = pd.read_csv('climat_apero.csv')

# Petit test d’affichage pour vérifier que le chargement a bien fonctionné
print("\nTest d'affichage :")
print(df.head())

# Affichage des statistiques descriptives de toutes les variables quantitatives
print("\nStatistiques descriptives :")
print(df.describe())

"""ANALYSE EXPLORATOIRE DES DONNÉES (EDA)"""
# On affiche une matrice de corrélation pour voir comment les variables sont liées entre elles
plt.figure(figsize=(12,10))
sns.heatmap(df.drop(columns=["Pays"]).corr(), annot=True, cmap="coolwarm")
plt.title("Matrice de Corrélation entre les Variables")
plt.show()

"""PRÉPARATION DE L’ACP (ANALYSE EN COMPOSANTES PRINCIPALES)"""
# On retire la colonne 'Pays' qui est qualitative et on ne garde que les variables quantitatives
X = df.drop(columns=["Pays"])

# Normalisation des données pour éviter que certaines variables dominent les autres à cause de leur échelle
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""ACP : CALCUL ET VISUALISATION"""
# On applique l’ACP sur les données normalisées
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Affichage de la variance expliquée par chaque composante
explained_variance = pca.explained_variance_ratio_
print("\nVariance expliquée par composante principale :")
for i, var in enumerate(explained_variance):
    print(f"Composante {i+1} : {var:.2%}")

# Courbe de l’éboulis (scree plot) pour identifier le nombre optimal de composantes à retenir
plt.figure(figsize=(8,6))
plt.plot(range(1, len(explained_variance)+1), explained_variance.cumsum(), marker='o')
plt.xlabel('Nombre de Composantes Principales')
plt.ylabel('Variance Cumulée')
plt.title('Scree Plot (Courbe de l’Éboulis)')
plt.grid()
plt.show()

"""VISUALISATION : CERCLE DES CORRÉLATIONS"""
# On visualise ici la projection des variables dans le plan des deux premières composantes
components = pca.components_

plt.figure(figsize=(8,8))
for i in range(len(X.columns)):
    plt.arrow(0, 0,
              components[0, i],
              components[1, i],
              head_width=0.03, head_length=0.03)
    plt.text(components[0, i]*1.1,
             components[1, i]*1.1,
             X.columns[i],
             color='red', ha='center', va='center')

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Cercle des Corrélations')
plt.axhline(0, color='grey', linestyle='--')
plt.axvline(0, color='grey', linestyle='--')
plt.grid()
plt.show()

"""STATISTIQUE INFÉRENTIELLE : TEST DE STUDENT"""
# On ajoute une colonne 'Europe' pour distinguer les pays européens du reste du monde
europe = ['France', 'Italie', 'Espagne', 'Allemagne', 'Portugal', 'Grèce', 'Autriche', 'Suisse',
          'Hongrie', 'Bulgarie', 'Roumanie', 'Croatie', 'Slovénie', 'Slovaquie', 'Chypre',
          'Serbie', 'Ukraine']
df['Europe'] = df['Pays'].apply(lambda x: 1 if x in europe else 0)

# Comparaison des températures moyennes entre pays européens et non-européens
group1 = df[df['Europe']==1]['Température (°C)']
group2 = df[df['Europe']==0]['Température (°C)']

# Test de Student pour comparer les moyennes des deux groupes
t_stat, p_value = stats.ttest_ind(group1, group2)

print("\nTest de Student entre Europe et Non-Europe sur Température :")
print(f"Statistique t : {t_stat:.4f}, p-value : {p_value:.4f}")
if p_value < 0.05:
    print("=> Différence significative")
else:
    print("=> Pas de différence significative")