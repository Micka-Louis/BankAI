import streamlit as st

st.set_page_config(
    page_title="Documentation | BankChurnAI",
    page_icon="📚",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .doc-section {
        background: white;
        padding: 2em;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1em 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5em;
        border-radius: 10px;
        text-align: center;
        margin: 0.5em 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# En-tête
st.title("📚 Documentation Technique")
st.markdown("### Méthodologie et Architecture du Système BankChurnAI")
st.markdown("---")

# Tabs pour organiser le contenu
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'Ensemble", 
    "🤖 Modèle ML", 
    "💡 Explicabilité", 
    "🎯 Recommandations",
    "🚀 Déploiement"
])

with tab1:
    st.markdown('<div class="doc-section">', unsafe_allow_html=True)
    st.markdown("""
    ## 🎯 Problématique
    
    Le **churn bancaire** (attrition client) représente un défi majeur pour les institutions financières en Haïti :
    - Coût d'acquisition d'un nouveau client : 5-7x plus élevé que la rétention
    - Impact direct sur la rentabilité et la croissance
    - Difficulté d'identifier les clients à risque avant leur départ
    
    ## 💡 Notre Solution
    
    BankChurnAI combine :
    1. **Machine Learning** : Prédiction précise du risque de churn
    2. **Explicabilité IA** : Compréhension des facteurs de décision (SHAP)
    3. **Recommandations Intelligentes** : Actions personnalisées par profil
    4. **Support Bilingue** : Interface FR/Kreyòl pour le contexte haïtien
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Architecture
    st.markdown("### 🏗️ Architecture du Système")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3>Collecte</h3>
            <p>15+ variables client</p>
            <p>Données comportementales, financières et contextuelles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3>Prédiction</h3>
            <p>Modèle CatBoost</p>
            <p>Probabilité de churn + facteurs SHAP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3>Action</h3>
            <p>Recommandations IA</p>
            <p>Stratégies personnalisées de rétention</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="doc-section">', unsafe_allow_html=True)
    st.markdown("""
    ## 🤖 Pipeline Machine Learning
    
    ### 📥 Données d'Entrée
    
    Notre modèle utilise **15+ variables** regroupées en 4 catégories :
    
    | Catégorie | Variables Clés |
    |-----------|---------------|
    | **Démographiques** | Âge, Genre, Éducation, Profession |
    | **Financières** | Revenu, Solde, Score Crédit, Transactions |
    | **Comportementales** | Connexions App, Mobile Money, Dernière Transaction |
    | **Contextuelles** | Région, Distance Agence, Transferts Diaspora |
    
    ### 🔧 Prétraitement
    
    1. **Encodage** : Variables catégorielles → One-Hot / Target Encoding
    2. **Normalisation** : StandardScaler pour variables numériques
    3. **Feature Engineering** : 
       - Ratio Solde/Revenu
       - Taux d'utilisation Mobile Money
       - Fréquence transactionnelle
    
    ### 🎯 Algorithme : CatBoost
    
    **Pourquoi CatBoost ?**
    - ✅ Gestion native des variables catégorielles
    - ✅ Robustesse au déséquilibre de classes
    - ✅ Performance supérieure (94.2% de précision)
    - ✅ Rapidité d'inférence (<10ms)
    
    **Hyperparamètres optimisés** :
    ```python
    {
        'iterations': 1000,
        'learning_rate': 0.05,
        'depth': 6,
        'l2_leaf_reg': 3,
        'class_weights': {0: 1, 1: 3}  # Gestion déséquilibre
    }
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Métriques de performance
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Précision", "94.2%", "+2.1%")
    with col2:
        st.metric("Recall", "89.5%", "+5.3%")
    with col3:
        st.metric("F1-Score", "91.7%", "+3.2%")
    with col4:
        st.metric("AUC-ROC", "0.95", "+0.03")

with tab3:
    st.markdown('<div class="doc-section">', unsafe_allow_html=True)
    st.markdown("""
    ## 💡 Explicabilité avec SHAP
    
    ### Qu'est-ce que SHAP ?
    
    **SHAP** (SHapley Additive exPlanations) calcule la contribution de chaque variable 
    à la prédiction finale en utilisant la théorie des jeux.
    
    ### 📊 Visualisations
    
    1. **Waterfall Plot** : Affiche comment chaque variable pousse la prédiction 
       vers "churn" ou "rétention"
       - 🔴 Rouge (→) : Augmente le risque
       - 🟢 Vert (←) : Diminue le risque
    
    2. **Interprétation** :
       ```
       Exemple : Client avec solde faible (5,000 HTG)
       → SHAP = +0.15 (pousse vers churn)
       
       Client avec 30+ connexions app/mois
       → SHAP = -0.22 (pousse vers rétention)
       ```
    
    ### ✨ Avantages
    
    - ✅ Transparence totale des décisions IA
    - ✅ Confiance accrue des agents bancaires
    - ✅ Identification des leviers d'action
    - ✅ Conformité réglementaire (IA explicable)
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="doc-section">', unsafe_allow_html=True)
    st.markdown("""
    ## 🎯 Système de Recommandations
    
    ### 🧠 Agent IA (LangChain + GPT)
    
    Notre agent génère des recommandations **personnalisées** basées sur :
    1. Probabilité de churn prédite
    2. Top 5 facteurs SHAP influents
    3. Profil client (Saver, Borrower, Digital Native...)
    4. Contexte haïtien (langue, culture, habitudes bancaires)
    
    ### 📋 Structure des Recommandations
    
    #### Risque FAIBLE (0-33%)
    - Stratégie : **Fidélisation**
    - Actions : Programmes VIP, offres exclusives
    - Fréquence : Trimestrielle
    
    #### Risque MOYEN (34-66%)
    - Stratégie : **Engagement**
    - Actions : Formation digitale, incentives
    - Fréquence : Mensuelle
    
    #### Risque ÉLEVÉ (67-100%)
    - Stratégie : **Rétention urgente**
    - Actions : Contact immédiat, offres personnalisées
    - Fréquence : Hebdomadaire
    
    ### 🌍 Support Bilingue
    
    - **Français** : Format professionnel, langage bancaire
    - **Kreyòl** : Ton accessible, termes locaux
    
    Exemple :
    - FR : "Proposez une réduction des frais de transfert"
    - HT : "Bay kliyan an pri pi ba pou vwayé lajan"
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="doc-section">', unsafe_allow_html=True)
    st.markdown("""
    ## 🚀 Déploiement & Infrastructure
    
    ### ☁️ Streamlit Cloud
    
    - **Plateforme** : Streamlit Community Cloud
    - **Runtime** : Python 3.11
    - **Ressources** : 1 GB RAM, partage public
    - **CI/CD** : Auto-deploy depuis GitHub
    
    ### 📦 Dépendances Clés
    
    ```txt
    streamlit==1.29.0
    scikit-learn==1.3.2
    catboost==1.2
    shap==0.44.0
    langchain==0.1.5
    ```
    
    ### 🔒 Sécurité & Performance
    
    - ✅ Secrets management (API keys)
    - ✅ Cache des prédictions (@st.cache_data)
    - ✅ Validation des inputs utilisateur
    - ✅ Temps de réponse < 50ms
    
    ### 📈 Monitoring
    
    - Nombre de prédictions / jour
    - Temps de réponse moyen
    - Distribution des probabilités
    - Taux d'utilisation par région
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Boutons de navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Retour Accueil", use_container_width=True):
        st.switch_page("Accueil.py")
with col2:
    if st.button("🎯 Tester le Modèle", type="primary", use_container_width=True):
        st.switch_page("pages/1_Prediction_Analyse.py")
