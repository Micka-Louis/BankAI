import streamlit as st

st.set_page_config(
    page_title="À Propos | BankChurnAI",
    page_icon="👥",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .member-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2em;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1em 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .member-card:hover {
        transform: scale(1.05);
    }
    .member-name {
        font-size: 1.5em;
        font-weight: bold;
        margin: 0.5em 0;
    }
    .member-role {
        font-size: 1.1em;
        opacity: 0.9;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# En-tête
st.title("👥 Équipe IMPACTIS")
st.markdown("### *Impact Through AI Solutions*")
st.markdown("---")

# Mission
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ## 🎯 Notre Mission
    
    Développer des solutions d'Intelligence Artificielle qui génèrent un **impact social positif** 
    en Haïti, tout en résolvant des problèmes concrets du secteur financier.
    
    **BankChurnAI** représente notre engagement à combiner innovation technologique et 
    développement économique local.
    """)

st.markdown("---")

# Membres de l'équipe
st.markdown("## 👨‍💻 Les Membres")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="member-card">
        <div style="font-size: 4em;">👨‍💼</div>
        <div class="member-name">Riché FLEURINORD</div>
        <div class="member-role">Data Scientist Lead</div>
        <br>
        <p>Expert en Machine Learning et optimisation de modèles prédictifs</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="member-card">
        <div style="font-size: 4em;">👨‍💻</div>
        <div class="member-name">Micka LOUIS</div>
        <div class="member-role">ML Engineer</div>
        <br>
        <p>Spécialiste en déploiement et infrastructure IA</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="member-card">
        <div style="font-size: 4em;">👨‍🔬</div>
        <div class="member-name">Vilmarson JULES</div>
        <div class="member-role">AI Researcher</div>
        <br>
        <p>Expert en explicabilité et recommandations intelligentes</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Contexte du projet
st.markdown("---")
st.markdown("## 🏆 Ayiti AI Hackathon 2025")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📅 Contexte
    - **Événement**: Ayiti AI Hackathon 2025
    - **Thème**: Solutions IA pour Haïti
    - **Défi**: Réduire le churn bancaire
    - **Durée**: 48 heures intensives
    """)

with col2:
    st.markdown("""
    ### 🎯 Objectifs Atteints
    - ✅ Modèle prédictif 94% de précision
    - ✅ Interface bilingue (FR/Kreyòl)
    - ✅ Explications SHAP détaillées
    - ✅ Déploiement cloud réussi
    """)

# Technologies
st.markdown("---")
st.markdown("## 🛠️ Stack Technologique")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **Machine Learning**
    - CatBoost
    - Scikit-learn
    - XGBoost
    - LightGBM
    """)

with col2:
    st.markdown("""
    **Explicabilité**
    - SHAP
    - Matplotlib
    - Seaborn
    """)

with col3:
    st.markdown("""
    **NLP & RAG**
    - LangChain
    - OpenAI GPT
    - Sentence Transformers
    """)

with col4:
    st.markdown("""
    **Déploiement**
    - Streamlit Cloud
    - GitHub
    - Python 3.11
    """)

# Contact
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ## 📧 Nous Contacter
    
    **GitHub**: [RicheFleurinord/BankChurnAI_Agent](https://github.com/RicheFleurinord/BankChurnAI_Agent)
    
    **Email**: team@impactis.ai
    
    ---
    
    *Fait avec ❤️ en Haïti 🇭🇹*
    """)

# Bouton retour
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🏠 Retour à l'Accueil", type="primary", use_container_width=True):
    st.switch_page("Accueil.py")
