import streamlit as st

st.title("📚 Documentation du Modèle")
st.markdown("""
Bienvenue dans la documentation de notre modèle. Vous trouverez ci-dessous des informations détaillées sur le jeu de données utilisé, la méthodologie, et les métriques de performance.
""")

# Section : Jeu de données
st.header("📊 Jeu de Données")
st.markdown("""
- **Source :** Indiquez ici la source de vos données (ex: Kaggle, Open Data, fichier interne, etc.)
- **Description :** Brève description du jeu de données et des variables principales.
- **Nombre d'observations :** Exemple : 10 000 lignes
- **Nombre de variables :** Exemple : 15 colonnes
""")

# Section : Méthodologie
st.header("🛠 Méthodologie")
st.markdown("""
1. **Prétraitement des données :**
   - Gestion des valeurs manquantes
   - Normalisation / Standardisation
   - Encodage des variables catégorielles
2. **Séparation des données :**
   - Train/Test split (ex: 80% / 20%)
3. **Modélisation :**
   - Algorithme utilisé (ex: Régression linéaire, Random Forest, XGBoost, etc.)
   - Paramètres principaux du modèle
4. **Validation :**
   - Validation croisée
   - Ajustement des hyperparamètres
""")

# Section : Métriques de performance
st.header("📈 Métriques de Performance")
st.markdown("""
- **Précision (Accuracy) :** xx %
- **Rappel (Recall) :** xx %
- **F1-score :** xx %
- **Matrice de confusion :** Illustration des vrais positifs, faux positifs, vrais négatifs, et faux négatifs
""")

# Section : Remarques finales
st.header("💡 Remarques")
st.markdown("""
- Ce modèle est destiné à être utilisé pour [votre objectif spécifique].
- Les résultats peuvent varier en fonction des nouvelles données ou de modifications des paramètres.
- Pour toute question ou contribution, contactez [votre email ou lien GitHub].
""")
