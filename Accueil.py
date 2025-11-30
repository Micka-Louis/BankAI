import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="BankChurnAI | IMPACTIS",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Animations et effets */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-title {
        text-align: center;
        font-size: 4em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 1s ease-out;
        margin-bottom: 0.5em;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.5em;
        color: #666;
        animation: fadeIn 1.2s ease-out;
        margin-bottom: 2em;
    }
    
    .hero-section {
        padding: 3em 0;
        text-align: center;
        animation: fadeIn 1.4s ease-out;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2em;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
    }
    
    .feature-card {
        background: white;
        padding: 2em;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        margin: 1em 0;
    }
    
    .feature-card:hover {
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transform: translateX(10px);
    }
    
    .team-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5em 1.5em;
        border-radius: 25px;
        font-weight: bold;
        margin: 0.5em;
    }
    
    /* Masquer les éléments Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# En-tête Hero
st.markdown('<h1 class="main-title">🏦 BankChurnAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligence Artificielle au Service de la Fidélisation Bancaire en Haïti 🇭🇹</p>', unsafe_allow_html=True)

# Section Hero
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### 🎯 Ayiti AI Hackathon 2025
    
    Une solution complète pour **prédire et prévenir** le départ des clients bancaires 
    grâce à l'apprentissage automatique et des recommandations personnalisées.
    
    **Propulsé par CatBoost • SHAP • LangChain**
    """)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Statistiques clés
st.markdown("### 📊 Performance du Modèle")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h2>94.2%</h2>
        <p>Précision</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h2>0.010s</h2>
        <p>Temps Prédiction</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h2>2 Langues</h2>
        <p>FR / Kreyòl</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h2>15+</h2>
        <p>Variables</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Fonctionnalités principales
st.markdown("### ✨ Fonctionnalités Clés")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Prédiction Intelligente</h3>
        <p>Modèle CatBoost optimisé pour le contexte haïtien avec une précision de 94%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Analyse SHAP</h3>
        <p>Visualisation interactive des facteurs influençant le risque de churn</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>💡 Recommandations Bilingues</h3>
        <p>Stratégies de rétention personnalisées en français et créole</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 Déploiement Immédiat</h3>
        <p>Interface intuitive pour les agents bancaires sans formation IA</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Boutons de navigation principaux
st.markdown("### 🚀 Commencer l'Analyse")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎯 LANCER PRÉDICTION", type="primary", use_container_width=True):
        st.switch_page("pages/1_Prediction_Analyse.py")
    st.caption("Analyser un profil client")

with col2:
    if st.button("📚 MÉTHODOLOGIE", use_container_width=True):
        st.switch_page("pages/2_Documentation.py")
    st.caption("Comprendre notre approche")

with col3:
    if st.button("👥 ÉQUIPE IMPACTIS", use_container_width=True):
        st.switch_page("pages/3_A_Propos.py")
    st.caption("Rencontrer les créateurs")

st.markdown("<br><br>", unsafe_allow_html=True)

# Section équipe
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h3>👥 Équipe IMPACTIS</h3>
        <span class="team-badge">Riché FLEURINORD</span>
        <span class="team-badge">Micka LOUIS</span>
        <span class="team-badge">Vilmarson JULES</span>
        <br><br>
        <p style="color: #666;">Ayiti AI Hackathon 2025 🇭🇹</p>
    </div>
    """, unsafe_allow_html=True)
