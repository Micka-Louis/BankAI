# pages/1_Prediction_Analyse.py - VERSION FINALE AVEC SHAP & RECOMMANDATIONS MULTILINGUES
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import os # Ajouté pour gestion des chemins

# --- Configuration et Chargement ---

# La configuration de la page se fait dans Accueil.py
st.title("🏦 Outil de Prédiction & Analyse de Churn")
st.subheader("Évaluation du risque client et plan d'action immédiat.")

# Sidebar
st.sidebar.title("🔧 Configuration")
st.sidebar.markdown("**Ayiti AI Hackathon 2025**")
st.sidebar.markdown("**Équipe IMPACTIS**")

# Chemins (Adapter le chemin car nous sommes dans un sous-dossier 'pages')
# On remonte d'un niveau pour trouver les fichiers .pkl et .json à la racine du dépôt
current_dir = Path(__file__).parent.parent 
model_path = current_dir / 'best_churn_model_pro_20251129_080606.pkl'
metadata_path = current_dir / 'model_metadata_pro_20251129_080606.json'
preprocessor_path = current_dir / 'preprocessor_pro_20251129_080606.pkl'

# Initialisation session
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'shap_plots' not in st.session_state:
    st.session_state.shap_plots = {}
if 'test_profile' not in st.session_state: # Maintenir l'initialisation du profil
    st.session_state.test_profile = None

# Chargement avec JOBLIB uniquement
@st.cache_resource(show_spinner="Chargement du modèle IA...")
def load_model():
    try:
        if not model_path.exists():
            st.sidebar.error(f"❌ Modèle non trouvé: {model_path.name}")
            return None
        
        model = joblib.load(model_path)
        st.sidebar.success("✅ Modèle IA chargé")
        return model
    except Exception as e:
        st.sidebar.error(f"❌ Erreur modèle: {str(e)}")
        return None

@st.cache_resource(show_spinner="Chargement du préprocesseur...")
def load_preprocessor():
    try:
        if not preprocessor_path.exists():
            return None
        
        preprocessor = joblib.load(preprocessor_path)
        st.sidebar.success("✅ Préprocesseur chargé")
        return preprocessor
    except Exception as e:
        st.sidebar.warning(f"⚠️ Préprocesseur: {str(e)}")
        return None

@st.cache_resource(show_spinner="Chargement des métadonnées...")
def load_metadata():
    try:
        if not metadata_path.exists():
            return {}
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        st.sidebar.success("✅ Métadonnées chargées")
        return data
    except Exception as e:
        st.sidebar.warning(f"⚠️ Métadonnées: {str(e)}")
        return {}

# Chargement
model = load_model()
preprocessor = load_preprocessor()
metadata = load_metadata()

# Affichage info modèle
if model is not None:
    st.sidebar.success("🎯 Système prêt!")
    
    if metadata:
        with st.sidebar.expander("📊 Infos Modèle", expanded=False):
            if 'model_info' in metadata:
                st.write(f"**Modèle:** {metadata['model_info'].get('best_model', 'N/A')}")
                st.write(f"**Stratégie:** {metadata['model_info'].get('best_strategy', 'N/A')}")
            
            if 'performance' in metadata:
                perf = metadata['performance']
                st.write(f"**AUC Test:** {perf.get('test_auc', 0):.4f}")
                st.write(f"**F1 Test:** {perf.get('test_f1', 0):.4f}")
                st.write(f"**Precision:** {perf.get('test_precision', 0):.4f}")
                st.write(f"**Recall:** {perf.get('test_recall', 0):.4f}")
else:
    st.sidebar.error("⚠️ Modèle non chargé")

# --- Définitions des Features ---
NUM_FEATURES = [
    "age", "household_size", "zone_security_level", "distance_to_branch_km",
    "income_monthly", "account_balance", "credit_score", "loan_balance",
    "transactions_count_monthly", "transfer_fees_paid", "time_with_bank_months",
    "last_transaction_days", "diaspora_transfers_received", "mobile_app_logins",
    "sentiment_score", "access_to_internet"
]

CAT_FEATURES = [
    "gender", "marital_status", "education_level", "profession",
    "region", "mobile_money_usage", "customer_persona_ai"
]

ALL_FEATURES_ORDERED = NUM_FEATURES + CAT_FEATURES

# --- Fonctions pour l'application des profils de test ---
def get_default_inputs():
    """Renvoie les valeurs par défaut du formulaire."""
    return {
        'age': 35, 'household_size': 3, 'zone_security_level': 2, 'distance_to_branch_km': 5.0,
        'income_monthly': 25000, 'account_balance': 50000, 'credit_score': 650, 'loan_balance': 0,
        'transactions_count_monthly': 15, 'transfer_fees_paid': 500, 'time_with_bank_months': 24, 'last_transaction_days': 7,
        'diaspora_transfers_received': 0, 'mobile_app_logins': 5, 'sentiment_score': 0.0, 'access_to_internet': "Oui",
        'gender': "M", 'marital_status': "Single", 'education_level': "University", 'profession': "Tech/Office",
        'region': "Ouest", 'mobile_money_usage': "Medium", 'customer_persona_ai': "Saver"
    }

def get_profile_inputs(profile_name):
    """Renvoie les valeurs pour un profil spécifique."""
    defaults = get_default_inputs()
    if profile_name == "fidele":
        return {
            **defaults,
            'age': 45, 'zone_security_level': 1, 'distance_to_branch_km': 2.0,
            'income_monthly': 120000, 'account_balance': 300000, 'credit_score': 780, 'loan_balance': 150000,
            'transactions_count_monthly': 35, 'transfer_fees_paid': 800, 'time_with_bank_months': 72, 'last_transaction_days': 2,
            'diaspora_transfers_received': 50000, 'mobile_app_logins': 25, 'sentiment_score': 0.8, 'access_to_internet': "Oui",
            'gender': "M", 'marital_status': "Married", 'education_level': "University", 'profession': "Civil Servant",
            'mobile_money_usage': "High", 'customer_persona_ai': "Premium",
        }
    elif profile_name == "risque":
        return {
            **defaults,
            'age': 28, 'household_size': 2, 'zone_security_level': 5, 'distance_to_branch_km': 35.0,
            'income_monthly': 15000, 'account_balance': 2000, 'credit_score': 380, 'loan_balance': 0,
            'transactions_count_monthly': 2, 'transfer_fees_paid': 50, 'time_with_bank_months': 6, 'last_transaction_days': 55,
            'diaspora_transfers_received': 0, 'mobile_app_logins': 0, 'sentiment_score': -0.8, 'access_to_internet': "Non",
            'gender': "F", 'marital_status': "Single", 'education_level': "Primary", 'profession': "Unemployed",
            'region': "Artibonite", 'mobile_money_usage': "Low", 'customer_persona_ai': "Cash User",
        }
    elif profile_name == "moyen":
        return {
            **defaults,
            'age': 38, 'household_size': 4, 'zone_security_level': 3, 'distance_to_branch_km': 8.0,
            'income_monthly': 45000, 'account_balance': 75000, 'credit_score': 620, 'loan_balance': 20000,
            'transactions_count_monthly': 12, 'transfer_fees_paid': 300, 'time_with_bank_months': 36, 'last_transaction_days': 18,
            'diaspora_transfers_received': 10000, 'mobile_app_logins': 8, 'sentiment_score': 0.1, 'access_to_internet': "Oui",
            'gender': "M", 'marital_status': "Married", 'education_level': "Secondary", 'profession': "Merchant",
            'region': "Nord", 'mobile_money_usage': "Medium", 'customer_persona_ai': "Trader",
        }
    return defaults

# Appliquer le profil sélectionné pour initialiser les widgets
if 'current_inputs' not in st.session_state:
    st.session_state.current_inputs = get_default_inputs()

# Si un profil de test a été cliqué (mis à jour par le bouton), mettez à jour les inputs
if st.session_state.test_profile:
    st.session_state.current_inputs = get_profile_inputs(st.session_state.test_profile)
    st.session_state.test_profile = None # Réinitialiser pour éviter la boucle

# --- Interface principale (Formulaire) ---
st.markdown("---")

with st.form(key='churn_form'):
    # Récupérer les inputs actuels pour pré-remplir le formulaire
    inputs = st.session_state.current_inputs

    # Formulaire client
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Informations Personnelles")
        
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            age = st.slider("Âge", 18, 80, inputs['age'], key='age_slider')
            gender = st.selectbox("Genre", ["M", "F"], index=["M", "F"].index(inputs['gender']), key='gender_select')
            marital_status = st.selectbox("Statut Matrimonial", ["Single", "Married", "Divorced", "Widowed"], index=["Single", "Married", "Divorced", "Widowed"].index(inputs['marital_status']), key='marital_select')
        with demo_col2:
            education_options = ["None", "Primary", "Secondary", "University", "Master/PhD"]
            education_level = st.selectbox("Niveau Éducation", education_options, index=education_options.index(inputs['education_level']), key='education_select')
            profession_options = ["Teacher", "Merchant", "Driver", "Civil Servant", "Health Worker", "Student", "Unemployed", "Tech/Office"]
            profession = st.selectbox("Profession", profession_options, index=profession_options.index(inputs['profession']), key='profession_select')
            household_size = st.slider("Taille Ménage", 1, 8, inputs['household_size'], key='household_slider')

    with col2:
        st.subheader("💳 Données Financières")
        
        finance_col1, finance_col2 = st.columns(2)
        with finance_col1:
            income_monthly = st.number_input("Revenu Mensuel (HTG)", 5000, 5000000, inputs['income_monthly'], 1000, key='income_input')
            account_balance = st.number_input("Solde Compte (HTG)", 0, 10000000, inputs['account_balance'], 1000, key='balance_input')
            credit_score = st.slider("Score Crédit", 300, 850, inputs['credit_score'], key='credit_slider')
            loan_balance = st.number_input("Solde Prêt (HTG)", 0, 5000000, inputs['loan_balance'], 1000, key='loan_input')
        with finance_col2:
            transactions_count_monthly = st.slider("Transactions/Mois", 0, 200, inputs['transactions_count_monthly'], key='transactions_slider')
            transfer_fees_paid = st.number_input("Frais Transfert (HTG)", 0, 50000, inputs['transfer_fees_paid'], 100, key='fees_input')
            time_with_bank_months = st.slider("Ancienneté (mois)", 1, 240, inputs['time_with_bank_months'], key='time_slider')
            last_transaction_days = st.slider("Dernière Transaction (jours)", 0, 90, inputs['last_transaction_days'], key='last_tx_slider')

    # Section comportementale
    st.markdown("---")
    st.subheader("📱 Comportement & Contexte")

    behavior_col1, behavior_col2, behavior_col3 = st.columns(3)

    with behavior_col1:
        mobile_app_logins = st.slider("Connexions App Mobile", 0, 50, inputs['mobile_app_logins'], key='logins_slider')
        diaspora_transfers_received = st.number_input("Transferts Diaspora (HTG)", 0, 1000000, inputs['diaspora_transfers_received'], 1000, key='diaspora_input')
        sentiment_score = st.slider("Score Sentiment", -1.0, 1.0, inputs['sentiment_score'], 0.1, key='sentiment_slider')

    with behavior_col2:
        zone_security_level = st.slider("Niveau Sécurité Zone", 1, 5, inputs['zone_security_level'], key='security_slider')
        distance_to_branch_km = st.slider("Distance Agence (km)", 0.0, 100.0, inputs['distance_to_branch_km'], 0.5, key='distance_slider')
        access_internet_choice = st.selectbox("Accès Internet", ["Oui", "Non"], index=["Oui", "Non"].index(inputs['access_to_internet']), key='internet_select')
        access_to_internet = 1 if access_internet_choice == "Oui" else 0

    with behavior_col3:
        mobile_money_options = ["Low", "Medium", "High"]
        mobile_money_usage = st.selectbox("Usage Mobile Money", mobile_money_options, index=mobile_money_options.index(inputs['mobile_money_usage']), key='mm_select')
        region_options = ["Ouest", "Artibonite", "Nord", "Sud", "Centre", "Grand'Anse", "Nord-Ouest", "Nord-Est", "Sud-Est", "Nippes"]
        region = st.selectbox("Région", region_options, index=region_options.index(inputs['region']), key='region_select')
        persona_options = ["Saver", "Trader", "Diaspora Dependent", "Digital Native", "Cash User", "Premium"]
        customer_persona_ai = st.selectbox("Profil Client", persona_options, index=persona_options.index(inputs['customer_persona_ai']), key='persona_select')

    # Bouton de soumission du formulaire
    analyze_clicked = st.form_submit_button("🎯 Analyser le Risque de Churn", type="primary", disabled=(model is None))

# --- Profils de Test (doivent être en dehors du formulaire pour utiliser st.rerun) ---
st.markdown("---")
st.subheader("🚀 Charger un Profil de Test")

test_col1, test_col2, test_col3, test_col4 = st.columns(4)

with test_col1:
    if st.button("🧪 Client Fidèle", use_container_width=True):
        st.session_state.test_profile = "fidele"
        st.rerun()

with test_col2:
    if st.button("⚠️ Client Risqué", use_container_width=True):
        st.session_state.test_profile = "risque"
        st.rerun()

with test_col3:
    if st.button("🔄 Client Moyen", use_container_width=True):
        st.session_state.test_profile = "moyen"
        st.rerun()

with test_col4:
    if st.button("📊 Réinitialiser les Inputs", use_container_width=True):
        st.session_state.current_inputs = get_default_inputs()
        st.rerun()

# --- Logique d'Analyse ---

if analyze_clicked and model is not None:
    # Sauvegarder les inputs actuels pour l'état de la session
    st.session_state.current_inputs = {
        'age': age, 'household_size': household_size, 'zone_security_level': zone_security_level,
        'distance_to_branch_km': distance_to_branch_km, 'income_monthly': income_monthly,
        'account_balance': account_balance, 'credit_score': credit_score, 'loan_balance': loan_balance,
        'transactions_count_monthly': transactions_count_monthly, 'transfer_fees_paid': transfer_fees_paid,
        'time_with_bank_months': time_with_bank_months, 'last_transaction_days': last_transaction_days,
        'diaspora_transfers_received': diaspora_transfers_received, 'mobile_app_logins': mobile_app_logins,
        'sentiment_score': sentiment_score, 'access_to_internet': access_internet_choice,
        'gender': gender, 'marital_status': marital_status, 'education_level': education_level,
        'profession': profession, 'region': region, 'mobile_money_usage': mobile_money_usage,
        'customer_persona_ai': customer_persona_ai
    }
    
    with st.spinner("🔍 Analyse en cours..."):
        try:
            start_time = time.time()
            
            # Données client pour la prédiction
            client_data = {
                'age': age, 'household_size': household_size, 'zone_security_level': zone_security_level,
                'distance_to_branch_km': distance_to_branch_km, 'income_monthly': income_monthly,
                'account_balance': account_balance, 'credit_score': credit_score, 'loan_balance': loan_balance,
                'transactions_count_monthly': transactions_count_monthly, 'transfer_fees_paid': transfer_fees_paid,
                'time_with_bank_months': time_with_bank_months, 'last_transaction_days': last_transaction_days,
                'diaspora_transfers_received': diaspora_transfers_received, 'mobile_app_logins': mobile_app_logins,
                'sentiment_score': sentiment_score, 'access_to_internet': access_to_internet,
                'gender': gender, 'marital_status': marital_status, 'education_level': education_level,
                'profession': profession, 'region': region, 'mobile_money_usage': mobile_money_usage,
                'customer_persona_ai': customer_persona_ai
            }
            
            # Prédiction
            df_client = pd.DataFrame([client_data])[ALL_FEATURES_ORDERED]
            proba = model.predict_proba(df_client)
            churn_proba = proba[0, 1]
            
            processing_time = time.time() - start_time
            
            # Affichage résultats
            st.success(f"✅ Analyse terminée en {processing_time:.3f}s")
            
            # Métriques
            col1, col2, col3, col4 = st.columns(4)
            
            if churn_proba < 0.3:
                delta_color, risk_label = "normal", "FAIBLE"
            elif churn_proba < 0.7:
                delta_color, risk_label = "off", "MOYEN"
            else:
                delta_color, risk_label = "inverse", "ÉLEVÉ"
            
            with col1:
                st.metric("Probabilité Churn", f"{churn_proba:.1%}", delta=risk_label, delta_color=delta_color)
            
            with col2:
                if churn_proba < 0.3:
                    risque_emoji, risque_text = "🟢", "FAIBLE"
                elif churn_proba < 0.7:
                    risque_emoji, risque_text = "🟡", "MOYEN"
                else:
                    risque_emoji, risque_text = "🔴", "ÉLEVÉ"
                st.metric("Niveau Risque", f"{risque_emoji} {risque_text}")
            
            with col3:
                prediction = "Restera" if churn_proba < 0.5 else "Partira"
                prediction_emoji = "✅" if churn_proba < 0.5 else "⚠️"
                st.metric("Prédiction", f"{prediction_emoji} {prediction}")
            
            with col4:
                confidence = max(churn_proba, 1 - churn_proba)
                st.metric("Confiance", f"{confidence:.1%}")
            
            # Barre de progression
            st.progress(float(churn_proba), text=f"Niveau de risque: {churn_proba:.1%}")
            
            # Section SHAP (Simulation)
            st.markdown("---")
            st.subheader("📊 Analyse SHAP - Facteurs d'Influence (Simulation)")
            
            # Calcul impacts basé sur les valeurs réelles (simulation SHAP)
            feature_impacts = {
                "Sentiment client": sentiment_score * -0.15,
                "Dernière transaction": (last_transaction_days / 90) * 0.12,
                "Niveau sécurité": (zone_security_level / 5) * 0.10,
                "Usage app mobile": (mobile_app_logins / 50) * -0.08,
                "Frais transfert": (transfer_fees_paid / 50000) * 0.07,
                "Score crédit": ((credit_score - 300) / 550) * -0.11,
                "Solde compte": (account_balance / 10000000) * -0.09,
                "Ancienneté": (time_with_bank_months / 240) * -0.06
            }
            
            sorted_features = sorted(feature_impacts.items(), key=lambda x: abs(x[1]), reverse=True)[:6]
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            features = [f[0] for f in sorted_features]
            impacts = [f[1] for f in sorted_features]
            importances = [abs(i) for i in impacts]
            
            y_pos = np.arange(len(features))
            
            # Importance
            ax1.barh(y_pos, importances, color='#3B82F6') # Utilisation du bleu
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(features)
            ax1.set_xlabel('Importance Absolue')
            ax1.set_title('Importance des Facteurs')
            ax1.invert_yaxis()
            
            # Impact
            colors = ['#EF4444' if x > 0 else '#10B981' for x in impacts] # Rouge et Vert Menthe
            ax2.barh(y_pos, impacts, color=colors)
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(features)
            ax2.set_xlabel('Impact sur Churn (Positif = Risque)')
            ax2.set_title('Direction de l\'Impact')
            ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            ax2.invert_yaxis()
            
            plt.tight_layout()
            st.pyplot(fig)
            
            st.info("""
            **🔍 Lecture SHAP (Simulée):**
            - **Rouge (→)**: Facteur qui **AUGMENTE** le risque de churn.
            - **Vert (←)**: Facteur qui **DIMINUE** le risque de churn.
            - **Taille**: Importance du facteur dans la décision.
            """)
            
            # Recommandations
            st.markdown("---")
            st.subheader("💡 Recommandations de Rétention (Multilingues)")
            
            risk_level = "FAIBLE" if churn_proba < 0.3 else "MOYEN" if churn_proba < 0.7 else "ÉLEVÉ"
            
            # Français
            with st.expander("🇫🇷 Recommandations en Français", expanded=True):
                if risk_level == "FAIBLE":
                    st.success("""
                    **Stratégie de Fidélisation:**
                    - ✅ Maintenir l'excellence dans la qualité de service.
                    - 🎁 Proposer des programmes fidélité premium.
                    - 📞 Effectuer un contact trimestriel proactif pour vérifier la satisfaction.
                    - 🌟 Offrir des avantages exclusifs et personnalisés (taux préférentiels).
                    
                    **Message suggéré:** "Merci pour votre fidélité ! Découvrez nos offres VIP."
                    """)
                elif risk_level == "MOYEN":
                    st.warning("""
                    **Stratégie de Consolidation:**
                    - 📞 Contact prioritaire dans les 7 jours pour une enquête de satisfaction.
                    - 🎯 Proposer des offres personnalisées pour augmenter l'engagement (ex: réduction de frais).
                    - 💻 Améliorer l'expérience digitale (ex: tutoriels, support mobile amélioré).
                    - 🤝 Mettre en place un programme de parrainage incitatif.
                    
                    **Message suggéré:** "Votre avis compte ! Parlons de vos besoins et de nos solutions."
                    """)
                else:
                    st.error("""
                    **🚨 URGENCE - Rétention Immédiate:**
                    - ☎️ Appel du gestionnaire de compte senior dans les 24 heures.
                    - 💰 Proposer une offre de rétention spéciale (ex: annulation de frais, meilleur taux).
                    - 🔍 Audit de compte complet pour identifier les irritants.
                    - 📊 Suivi intensif et personnalisé sur 30 jours.
                    
                    **Message suggéré:** "Priorité absolue ! Contactez-nous immédiatement pour résoudre la situation."
                    """)
            
            # Créole
            with st.expander("🇭🇹 Rekòmandasyon an Kreyòl", expanded=False):
                if risk_level == "FAIBLE":
                    st.success("""
                    **Estratèj Fidelite:**
                    - ✅ Kenbe bon jan kalite sèvis la.
                    - 🎁 Pwopoze pwogram fidelite primòm.
                    - 📞 Rele chak twa mwa pou tcheke satisfaksyon.
                    - 🌟 Bay avantaj espesyal ak pèsonalize (to preferansyèl).
                    
                    **Mesaj:** "Mèsi pou fidelite w! Dekouvri òf VIP nou yo."
                    """)
                elif risk_level == "MOYEN":
                    st.warning("""
                    **Estratèj Konsolidasyon:**
                    - 📞 Rele an priyorite nan 7 jou pou fè yon ankèt.
                    - 🎯 Pwopoze òf pèsonalize pou ogmante angajman (egzanp: rediksyon frè).
                    - 💻 Amelyore eksperyans dijital la (egzanp: sipò mobil pi bon).
                    - 🤝 Mete yon pwogram parennaj ak ankourajman.
                    
                    **Mesaj:** "Opinyon w enpòtan! Ann pale de bezwen w ak solisyon nou yo."
                    """)
                else:
                    st.error("""
                    **🚨 IJAN - Retansyon Imedya:**
                    - ☎️ Manadjè kont la dwe rele nan 24 èdtan.
                    - 💰 Pwopoze yon òf espesyal pou retansyon (egzanp: anile frè, pi bon to).
                    - 🔍 Verifye kont konplè pou idantifye pwoblèm yo.
                    - 📊 Fè yon swivi entansif ak pèsonalize sou 30 jou.
                    
                    **Mesaj:** "Priyorite absoli! Kontakte nou kounye a pou nou rezoud sitiyasyon an."
                    """)
            
            # Plan d'action
            st.markdown("---")
            st.subheader("🎯 Plan d'Action Opérationnel")
            
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                st.write("**⏰ Actions Immédiates (0-48h):**")
                if risk_level == "ÉLEVÉ":
                    st.markdown("""
                    1. 🚨 **Alerte gestionnaire** - Notification push au responsable.
                    2. ☎️ **Appel personnel** - Utiliser un script de rétention agressif.
                    3. 💰 **Offre immédiate** - Lancer la procédure d'offre spéciale.
                    4. 📝 **Documentation** - Enregistrer le risque dans le CRM.
                    """)
                else:
                    st.markdown("""
                    1. 📅 **Planifier contact** - Fixer une date pour le prochain appel de courtoisie.
                    2. 📊 **Analyser profil** - Revoir l'historique d'utilisation des produits.
                    3. 🎯 **Préparer offres** - Identifier 2 produits à proposer.
                    4. 💻 **Check digital** - Vérifier l'activation des outils digitaux.
                    """)
            
            with action_col2:
                st.write("**📈 Actions Moyen Terme (1-30 jours):**")
                st.markdown("""
                1. 🔄 **Suivi régulier** - Touchpoints pour vérifier l'efficacité des actions.
                2. 🎁 **Programme fidélité** - Intégration ou montée en gamme dans le programme.
                3. 📚 **Formation** - Encourager l'utilisation d'un produit sous-utilisé.
                4. 🤝 **Relation client** - Mettre en place une relation client proactive.
                5. 📊 **KPIs** - Monitoring continu du score de risque.
                """)
            
            # Historique et Export
            analysis_record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "churn_probability": float(churn_proba),
                "risk_level": risk_level,
                "processing_time": float(processing_time),
                "client_id": f"CLT_{int(time.time())}"
            }
            st.session_state.analysis_history.append(analysis_record)
            
            st.markdown("---")
            if st.button("📥 Exporter l'Analyse Détaillée (JSON)"):
                export_data = {
                    "client_data": client_data,
                    "prediction": {
                        "churn_probability": float(churn_proba),
                        "risk_level": risk_level,
                        "confidence": float(confidence)
                    },
                    "feature_impacts": {k: float(v) for k, v in feature_impacts.items()},
                    "timestamp": datetime.now().isoformat()
                }
                # Pour éviter le second bouton de téléchargement, on utilise un conteneur temporaire
                st.download_button(
                    "💾 Télécharger JSON",
                    data=json.dumps(export_data, indent=2, ensure_ascii=False),
                    file_name=f"churn_analysis_{int(time.time())}.json",
                    mime="application/json"
                )
            
        except Exception as e:
            st.error(f"❌ ERREUR LORS DE L'ANALYSE: {str(e)}")
            with st.expander("🔍 Détails techniques"):
                import traceback
                st.code(traceback.format_exc())

elif analyze_clicked:
    st.error("❌ Le modèle de prédiction n'a pas pu être chargé. Vérifiez les fichiers.")

# Historique
if st.session_state.analysis_history:
    st.markdown("---")
    with st.expander(f"📜 Historique des Analyses ({len(st.session_state.analysis_history)})"):
        df_history = pd.DataFrame(st.session_state.analysis_history)
        # Afficher les 10 dernières analyses
        st.dataframe(df_history.sort_values('timestamp', ascending=False).head(10), use_container_width=True)

# CSS pour le style local à cette page
st.markdown("""
<style>
    .stButton>button { width: 100%; }
    h1 { color: #1E3A8A; }
    h2 { color: #2563EB; }
</style>
""", unsafe_allow_html=True)
