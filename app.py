"""
NEXUS - Système RAMA
Application Streamlit complète avec logique hiérarchique avancée
Charte graphique Orange : #FF7900, Noir, Blanc
Compatible Google Colab via pyngrok
"""

# ============================================================
# INSTALLATION (décommenter pour Google Colab)
# ============================================================
# !pip install streamlit pyngrok --quiet

import sqlite3
import hashlib
import os
import threading
from datetime import date, datetime

# ============================================================
# STREAMLIT EN MODE COLAB — décommenter si Colab
# ============================================================
# from pyngrok import ngrok
# import subprocess
# subprocess.Popen(["streamlit", "run", __file__, "--server.port=8501"])
# public_url = ngrok.connect(8501)
# print("URL publique :", public_url)

import streamlit as st

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="NEXUS — Système RAMA",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CHARTE GRAPHIQUE ORANGE
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;900&family=Barlow+Condensed:wght@700;900&display=swap');

:root {
    --orange: #FF7900;
    --orange-dark: #CC6100;
    --orange-light: #FFB366;
    --black: #000000;
    --dark: #1A1A1A;
    --mid: #333333;
    --gray: #666666;
    --light-gray: #F5F5F5;
    --white: #FFFFFF;
}

* { font-family: 'Barlow', sans-serif; }

/* Fond général */
.stApp { background-color: var(--light-gray); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--black) !important;
    border-right: 3px solid var(--orange);
}
section[data-testid="stSidebar"] * { color: var(--white) !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label { color: var(--white) !important; }

/* Titres */
h1, h2, h3 { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 900 !important; }
h1 { color: var(--orange) !important; font-size: 2.8rem !important; letter-spacing: -1px; }
h2 { color: var(--dark) !important; font-size: 1.8rem !important; }
h3 { color: var(--mid) !important; font-size: 1.3rem !important; }

/* Boutons principaux */
.stButton > button {
    background: var(--orange) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.2s ease;
    letter-spacing: 0.5px;
}
.stButton > button:hover {
    background: var(--orange-dark) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(255,121,0,0.35) !important;
}

/* Inputs */
/* Correction pour rendre le texte bien visible en noir */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    border: 2px solid #FF7900 !important; /* Bordure orange pour le style */
    -webkit-text-fill-color: #000000 !important;
}

/* Texte des labels (noms des champs) en noir */
label[data-testid="stWidgetLabel"] p {
    color: #000000 !important;
    font-weight: bold !important;
}

/* Métriques */
[data-testid="stMetric"] {
    background: var(--white);
    border: 2px solid var(--orange);
    border-radius: 8px;
    padding: 1rem !important;
}
[data-testid="stMetric"] label { color: var(--gray) !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: var(--orange) !important; font-weight: 900 !important; font-size: 2rem !important; }

/* Cards personnalisées */
.nexus-card {
    background: var(--white);
    border-left: 5px solid var(--orange);
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.nexus-card-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--dark);
    margin-bottom: 0.3rem;
}
.nexus-card-sub { color: var(--gray); font-size: 0.88rem; }

/* Badges statut */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-actif      { background: #E8F5E9; color: #2E7D32; }
.badge-inactif    { background: #FFEBEE; color: #C62828; }
.badge-pause      { background: #FFF3E0; color: #E65100; }
.badge-planifiee  { background: #E3F2FD; color: #1565C0; }
.badge-encours    { background: #FFF9C4; color: #F57F17; }
.badge-terminee   { background: #E8F5E9; color: #2E7D32; }
.badge-annulee    { background: #F5F5F5; color: #616161; }
.badge-haute      { background: #FFEBEE; color: #C62828; }
.badge-moyenne    { background: #FFF3E0; color: #E65100; }
.badge-faible     { background: #F5F5F5; color: #616161; }

/* Bandeau header */
.nexus-header {
    background: var(--black);
    color: var(--white);
    padding: 1rem 2rem;
    margin-bottom: 1.5rem;
    border-bottom: 4px solid var(--orange);
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 6px;
}
.nexus-logo {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 900;
    font-size: 2rem;
    color: var(--orange);
    letter-spacing: 2px;
}
.nexus-user-info { font-size: 0.9rem; color: #CCC; }

/* Notifications */
.notif-item {
    background: #FFF3E0;
    border-left: 4px solid var(--orange);
    padding: 0.8rem 1rem;
    border-radius: 4px;
    margin-bottom: 0.6rem;
}
.notif-title { font-weight: 700; color: var(--dark); font-size: 0.95rem; }
.notif-desc  { color: var(--gray); font-size: 0.85rem; margin-top: 2px; }
.notif-date  { color: #AAA; font-size: 0.78rem; margin-top: 4px; }

/* Séparateur orange */
.orange-sep {
    height: 3px;
    background: linear-gradient(to right, var(--orange), transparent);
    margin: 1.5rem 0;
    border: none;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--white) !important;
    border: 2px solid #EEE !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    color: var(--dark) !important;
}
.streamlit-expanderHeader:hover { border-color: var(--orange) !important; }

/* Tables */
.stDataFrame { border-radius: 6px; overflow: hidden; }

/* Success / Error / Info */
.stAlert { border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# BASE DE DONNÉES — INITIALISATION
# ============================================================
DB_PATH = "nexus.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS Service (
        id_service   INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_service  VARCHAR(100) NOT NULL UNIQUE,
        description  TEXT
    );

    CREATE TABLE IF NOT EXISTS Agent (
        id_agent            INTEGER PRIMARY KEY AUTOINCREMENT,
        nom                 VARCHAR(20)  NOT NULL,
        prenom              VARCHAR(30)  NOT NULL,
        niveau_hierarchique VARCHAR(50)  NOT NULL
                            CHECK (niveau_hierarchique IN ('PDG','Directeur General','Chef de service','Operant')),
        mail                VARCHAR(50)  NOT NULL UNIQUE,
        numero_telephone    VARCHAR(20),
        statut              VARCHAR(20)  NOT NULL DEFAULT 'actif'
                            CHECK (statut IN ('actif','pause','inactif')),
        est_directeur       INTEGER NOT NULL DEFAULT 0
                            CHECK (est_directeur IN (0,1)),
        id_service          INTEGER,
        id_agent_chef       INTEGER,
        mot_de_passe        VARCHAR(64),
        FOREIGN KEY (id_service)    REFERENCES Service(id_service),
        FOREIGN KEY (id_agent_chef) REFERENCES Agent(id_agent)
    );

    CREATE TABLE IF NOT EXISTS Activite (
        id_activite  INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_activite VARCHAR(150) NOT NULL,
        type_activite VARCHAR(50) NOT NULL,
        date_debut   DATE NOT NULL,
        date_fin     DATE NOT NULL,
        statut       VARCHAR(30) NOT NULL DEFAULT 'planifiee'
                     CHECK (statut IN ('planifiee','en cours','terminee','annulee')),
        id_service   INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES Service(id_service)
    );

    CREATE TABLE IF NOT EXISTS PARTICIPATION (
        id_agent    INTEGER NOT NULL,
        id_activite INTEGER NOT NULL,
        PRIMARY KEY (id_agent, id_activite),
        FOREIGN KEY (id_agent)    REFERENCES Agent(id_agent),
        FOREIGN KEY (id_activite) REFERENCES Activite(id_activite)
    );

    CREATE TABLE IF NOT EXISTS Tache (
        id_tache          INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_tache         VARCHAR(150) NOT NULL,
        description       TEXT,
        date_debut_prevue DATE NOT NULL,
        date_fin_prevue   DATE NOT NULL,
        date_debut_reelle DATE,
        date_fin_reelle   DATE,
        priorite          VARCHAR(20) NOT NULL DEFAULT 'moyenne'
                          CHECK (priorite IN ('faible','moyenne','haute')),
        statut            VARCHAR(30) NOT NULL DEFAULT 'non demarree'
                          CHECK (statut IN ('non demarree','en cours','terminee','annulee')),
        id_activite       INTEGER NOT NULL,
        id_agent_assigne  INTEGER NOT NULL,
        id_agent_effectue INTEGER NOT NULL,
        FOREIGN KEY (id_activite)       REFERENCES Activite(id_activite),
        FOREIGN KEY (id_agent_assigne)  REFERENCES Agent(id_agent),
        FOREIGN KEY (id_agent_effectue) REFERENCES Agent(id_agent)
    );

    CREATE TABLE IF NOT EXISTS INDICATEUR_PERFORMANCE (
        id_indicateur   INTEGER PRIMARY KEY AUTOINCREMENT,
        periode         VARCHAR(50) NOT NULL,
        nb_tache_assigne INTEGER DEFAULT 0,
        nb_tache_termine INTEGER DEFAULT 0,
        nb_tache_retard  INTEGER DEFAULT 0,
        id_tache         INTEGER NOT NULL,
        FOREIGN KEY (id_tache) REFERENCES Tache(id_tache)
    );

    CREATE TABLE IF NOT EXISTS HISTORIQUE (
        id_historique   INTEGER PRIMARY KEY AUTOINCREMENT,
        date_historique DATE NOT NULL,
        type_changement VARCHAR(50) NOT NULL
                        CHECK (type_changement IN ('affectation','reaffectation','retrait')),
        motif           TEXT,
        id_tache        INTEGER NOT NULL,
        FOREIGN KEY (id_tache) REFERENCES Tache(id_tache)
    );

    CREATE TABLE IF NOT EXISTS NOTIFICATION (
        id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
        titre           VARCHAR(150) NOT NULL,
        description     TEXT NOT NULL,
        date_envoie     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        statut          VARCHAR(30) NOT NULL DEFAULT 'envoyee'
                        CHECK (statut IN ('envoyee','lue','archivee')),
        id_agent        INTEGER NOT NULL,
        id_activite     INTEGER,
        id_tache        INTEGER,
        FOREIGN KEY (id_agent)    REFERENCES Agent(id_agent),
        FOREIGN KEY (id_activite) REFERENCES Activite(id_activite),
        FOREIGN KEY (id_tache)    REFERENCES Tache(id_tache)
    );

    CREATE TABLE IF NOT EXISTS AVIS (
        id_avis                 INTEGER PRIMARY KEY AUTOINCREMENT,
        titre                   VARCHAR(150) NOT NULL,
        contenu                 TEXT NOT NULL,
        note                    INTEGER CHECK (note BETWEEN 1 AND 5),
        fonctionnalite_concernee TEXT,
        date_avis               DATE DEFAULT (CURRENT_DATE),
        id_agent                INTEGER NOT NULL,
        FOREIGN KEY (id_agent) REFERENCES Agent(id_agent)
    );

    CREATE TABLE IF NOT EXISTS Boite_idee (
        id_idee  INTEGER PRIMARY KEY AUTOINCREMENT,
        titre    VARCHAR(150) NOT NULL,
        contenu  TEXT NOT NULL,
        domaine  TEXT,
        statut   VARCHAR(30) NOT NULL DEFAULT 'soumise'
                 CHECK (statut IN ('soumise','en etude','acceptee','rejetee')),
        id_agent INTEGER NOT NULL,
        FOREIGN KEY (id_agent) REFERENCES Agent(id_agent)
    );

    CREATE TABLE IF NOT EXISTS Signalement (
        id_signalement  INTEGER PRIMARY KEY AUTOINCREMENT,
        titre           VARCHAR(150) NOT NULL,
        description     TEXT NOT NULL,
        niveau_urgence  VARCHAR(20) NOT NULL
                        CHECK (niveau_urgence IN ('faible','moyen','urgent')),
        statut          VARCHAR(30) NOT NULL DEFAULT 'ouvert'
                        CHECK (statut IN ('ouvert','en traitement','resolu','ferme')),
        date_signalement DATE DEFAULT (CURRENT_DATE),
        id_agent         INTEGER NOT NULL,
        FOREIGN KEY (id_agent) REFERENCES Agent(id_agent)
    );
    """)

    # Compte PDG par défaut
    existing = c.execute("SELECT id_agent FROM Agent WHERE mail='pdg@nexus.sn'").fetchone()
    if not existing:
        c.execute("""
            INSERT INTO Agent (nom, prenom, niveau_hierarchique, mail, statut, est_directeur, mot_de_passe)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("PAPA", "DIOP", "PDG", "pdg@nexus.sn", "actif", 1, hash_password("nexus123")))

    conn.commit()
    conn.close()

init_db()

# ============================================================
# SESSION STATE
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "agent" not in st.session_state:
    st.session_state.agent = None
if "ops_service_id" not in st.session_state:
    st.session_state.ops_service_id = None
if "ops_agent_id" not in st.session_state:
    st.session_state.ops_agent_id = None

# ============================================================
# HELPERS BD
# ============================================================
def fetch_all(query, params=()):
    conn = get_conn()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows

def fetch_one(query, params=()):
    conn = get_conn()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return row

def execute_query(query, params=()):
    conn = get_conn()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id

def badge_html(text, cls):
    return f'<span class="badge badge-{cls}">{text}</span>'

def statut_badge(statut):
    mapping = {
        "actif": "actif", "inactif": "inactif", "pause": "pause",
        "planifiee": "planifiee", "en cours": "encours",
        "terminee": "terminee", "annulee": "annulee",
        "haute": "haute", "moyenne": "moyenne", "faible": "faible",
        "non demarree": "planifiee",
    }
    cls = mapping.get(statut, "planifiee")
    return badge_html(statut.upper(), cls)

def send_notification(id_agent, titre, description, id_activite=None, id_tache=None):
    execute_query("""
        INSERT INTO NOTIFICATION (titre, description, id_agent, id_activite, id_tache)
        VALUES (?, ?, ?, ?, ?)
    """, (titre, description, id_agent, id_activite, id_tache))

# ============================================================
# PAGE LOGIN
# ============================================================
def page_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom:2rem;">
            <div style="font-family:'Barlow Condensed',sans-serif; font-weight:900;
                        font-size:3.5rem; color:#FF7900; letter-spacing:4px;">NEXUS</div>
            <div style="color:#666; font-size:1rem; letter-spacing:2px; text-transform:uppercase;">
                Système RAMA — Plateforme de Gestion
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style="background:#FFF; border:2px solid #EEE; border-top:5px solid #FF7900;
                        border-radius:8px; padding:2rem 2rem 1.5rem;">
            """, unsafe_allow_html=True)

            st.markdown("### 🔐 Connexion")
            email = st.text_input("Adresse email", placeholder="votre@email.sn")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")

            if st.button("Se connecter", use_container_width=True):
                if not email or not password:
                    st.error("Veuillez renseigner tous les champs.")
                else:
                    agent = fetch_one(
                        "SELECT * FROM Agent WHERE mail=? AND mot_de_passe=? AND statut='actif'",
                        (email, hash_password(password))
                    )
                    if agent:
                        st.session_state.authenticated = True
                        st.session_state.agent = dict(agent)
                        st.rerun()
                    else:
                        st.error("Email ou mot de passe incorrect, ou compte inactif.")

            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center;color:#AAA;font-size:0.8rem;'>© 2025 NEXUS — Système RAMA</div>",
            unsafe_allow_html=True
        )

# ============================================================
# HEADER COMMUN
# ============================================================
def render_header():
    agent = st.session_state.agent
    niveau = agent["niveau_hierarchique"]
    nom_complet = f"{agent['prenom']} {agent['nom']}"
    st.markdown(f"""
    <div class="nexus-header">
        <div class="nexus-logo">⬛ NEXUS</div>
        <div class="nexus-user-info">
            👤 <strong style="color:#FF7900;">{nom_complet}</strong> &nbsp;|&nbsp;
            🎖️ {niveau} &nbsp;|&nbsp;
            📅 {date.today().strftime('%d/%m/%Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
def get_menu_items(niveau):
    base = ["🏠 Tableau de Bord", "🔔 Notifications", "💡 Boîte à Idées", "⚠️ Signalements", "⭐ Avis"]
    if niveau == "PDG":
        return ["🏠 Tableau de Bord", "👥 Gestion Agents", "🏢 Services",
                "📋 Activités", "🗂️ Tâches", "📊 Opérations",
                "🔔 Notifications", "💡 Boîte à Idées", "⚠️ Signalements", "⭐ Avis"]
    elif niveau == "Directeur General":
        return ["🏠 Tableau de Bord", "👥 Gestion Agents", "🏢 Services",
                "📋 Activités", "🗂️ Tâches", "📊 Opérations",
                "🔔 Notifications", "💡 Boîte à Idées", "⚠️ Signalements", "⭐ Avis"]
    elif niveau == "Chef de service":
        return ["🏠 Tableau de Bord", "🗂️ Tâches", "📊 Opérations",
                "🔔 Notifications", "💡 Boîte à Idées", "⚠️ Signalements", "⭐ Avis"]
    else:  # Operant
        return ["🏠 Tableau de Bord", "🗂️ Mes Tâches", "🔔 Notifications",
                "💡 Boîte à Idées", "⚠️ Signalements", "⭐ Avis"]

# ============================================================
# TABLEAU DE BORD
# ============================================================
def page_dashboard():
    render_header()
    agent = st.session_state.agent
    niveau = agent["niveau_hierarchique"]
    st.markdown("## 🏠 Tableau de Bord")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    if niveau in ("PDG", "Directeur General"):
        c1, c2, c3, c4 = st.columns(4)
        nb_agents     = fetch_one("SELECT COUNT(*) as n FROM Agent")[0]
        nb_services   = fetch_one("SELECT COUNT(*) as n FROM Service")[0]
        nb_activites  = fetch_one("SELECT COUNT(*) as n FROM Activite")[0]
        nb_taches     = fetch_one("SELECT COUNT(*) as n FROM Tache")[0]
        with c1: st.metric("👥 Agents", nb_agents)
        with c2: st.metric("🏢 Services", nb_services)
        with c3: st.metric("📋 Activités", nb_activites)
        with c4: st.metric("🗂️ Tâches", nb_taches)

        st.markdown("### 📋 Activités récentes")
        activites = fetch_all("""
            SELECT a.nom_activite, a.statut, a.date_debut, a.date_fin, s.nom_service
            FROM Activite a JOIN Service s ON a.id_service=s.id_service
            ORDER BY a.id_activite DESC LIMIT 5
        """)
        for act in activites:
            st.markdown(f"""
            <div class="nexus-card">
                <div class="nexus-card-title">{act['nom_activite']}</div>
                <div class="nexus-card-sub">
                    🏢 {act['nom_service']} &nbsp;|&nbsp;
                    📅 {act['date_debut']} → {act['date_fin']} &nbsp;|&nbsp;
                    {statut_badge(act['statut'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif niveau == "Chef de service":
        id_service = agent.get("id_service")
        c1, c2, c3 = st.columns(3)
        nb_op   = fetch_one("SELECT COUNT(*) FROM Agent WHERE id_service=? AND niveau_hierarchique='Operant'", (id_service,))[0]
        nb_act  = fetch_one("SELECT COUNT(*) FROM Activite WHERE id_service=?", (id_service,))[0]
        nb_t    = fetch_one("""
            SELECT COUNT(*) FROM Tache t
            JOIN Activite a ON t.id_activite=a.id_activite
            WHERE a.id_service=?
        """, (id_service,))[0]
        with c1: st.metric("👷 Opérants", nb_op)
        with c2: st.metric("📋 Activités du service", nb_act)
        with c3: st.metric("🗂️ Tâches", nb_t)

        st.markdown("### 🗂️ Tâches en cours dans votre service")
        taches = fetch_all("""
            SELECT t.nom_tache, t.statut, t.priorite,
                   ag.prenom || ' ' || ag.nom AS agent_nom
            FROM Tache t
            JOIN Activite a ON t.id_activite=a.id_activite
            JOIN Agent ag ON t.id_agent_effectue=ag.id_agent
            WHERE a.id_service=? AND t.statut='en cours'
            LIMIT 10
        """, (id_service,))
        for t in taches:
            st.markdown(f"""
            <div class="nexus-card">
                <div class="nexus-card-title">{t['nom_tache']}</div>
                <div class="nexus-card-sub">
                    👤 {t['agent_nom']} &nbsp;|&nbsp;
                    Priorité : {statut_badge(t['priorite'])} &nbsp;|&nbsp;
                    {statut_badge(t['statut'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:  # Opérant
        id_agent = agent["id_agent"]
        c1, c2, c3 = st.columns(3)
        total  = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=?", (id_agent,))[0]
        done   = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=? AND statut='terminee'", (id_agent,))[0]
        encours = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=? AND statut='en cours'", (id_agent,))[0]
        with c1: st.metric("📦 Total tâches", total)
        with c2: st.metric("✅ Terminées", done)
        with c3: st.metric("⚙️ En cours", encours)

        # Notifications non lues
        notifs = fetch_all("""
            SELECT * FROM NOTIFICATION WHERE id_agent=? AND statut='envoyee'
            ORDER BY date_envoie DESC
        """, (id_agent,))
        if notifs:
            st.warning(f"🔔 Vous avez **{len(notifs)}** nouvelle(s) notification(s) !")
            for n in notifs:
                st.markdown(f"""
                <div class="notif-item">
                    <div class="notif-title">🔔 {n['titre']}</div>
                    <div class="notif-desc">{n['description']}</div>
                    <div class="notif-date">{n['date_envoie']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"✔ Marquer comme lue", key=f"lu_{n['id_notification']}"):
                    execute_query("UPDATE NOTIFICATION SET statut='lue' WHERE id_notification=?", (n['id_notification'],))
                    st.rerun()

# ============================================================
# GESTION AGENTS
# ============================================================
def page_agents():
    render_header()
    agent = st.session_state.agent
    niveau = agent["niveau_hierarchique"]
    st.markdown("## 👥 Gestion des Agents")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Liste des agents", "➕ Ajouter un agent"])

    with tab1:
        agents = fetch_all("""
            SELECT a.*, s.nom_service,
                   ch.prenom || ' ' || ch.nom AS chef_nom
            FROM Agent a
            LEFT JOIN Service s ON a.id_service=s.id_service
            LEFT JOIN Agent ch ON a.id_agent_chef=ch.id_agent
            ORDER BY a.niveau_hierarchique, a.nom
        """)
        for ag in agents:
            with st.expander(f"👤 {ag['prenom']} {ag['nom']} — {ag['niveau_hierarchique']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Email :** {ag['mail']}")
                    st.markdown(f"**Tél :** {ag['numero_telephone'] or '—'}")
                    st.markdown(f"**Service :** {ag['nom_service'] or '—'}")
                with c2:
                    st.markdown(f"**Statut :** {ag['statut']}", unsafe_allow_html=True)
                    st.markdown(f"**Chef direct :** {ag['chef_nom'] or '—'}")
                    st.markdown(f"**Directeur :** {'Oui' if ag['est_directeur'] else 'Non'}")

                # Modifier statut
                if niveau in ("PDG", "Directeur General"):
                    new_statut = st.selectbox("Changer statut", ["actif", "pause", "inactif"],
                                              index=["actif", "pause", "inactif"].index(ag["statut"]),
                                              key=f"statut_{ag['id_agent']}")
                    if st.button("💾 Mettre à jour", key=f"upd_{ag['id_agent']}"):
                        execute_query("UPDATE Agent SET statut=? WHERE id_agent=?", (new_statut, ag["id_agent"]))
                        st.success("Statut mis à jour.")
                        st.rerun()

    with tab2:
        st.markdown("### ➕ Créer un nouvel agent")
        services = fetch_all("SELECT * FROM Service ORDER BY nom_service")
        agents_chefs = fetch_all("SELECT * FROM Agent WHERE niveau_hierarchique IN ('PDG','Directeur General','Chef de service') ORDER BY nom")

        c1, c2 = st.columns(2)
        with c1:
            nom    = st.text_input("Nom *")
            prenom = st.text_input("Prénom *")
            mail   = st.text_input("Email *")
            telephone = st.text_input("Téléphone")
        with c2:
            niveaux = ["Directeur General", "Chef de service", "Operant"]
            if niveau == "PDG":
                niveaux = ["PDG"] + niveaux
            niveau_new = st.selectbox("Niveau hiérarchique *", niveaux)
            mdp = st.text_input("Mot de passe *", type="password")
            est_dir = st.checkbox("Est directeur de service ?")
            service_names = ["— Aucun —"] + [s["nom_service"] for s in services]
            sel_service = st.selectbox("Service", service_names)
            chef_names = ["— Aucun —"] + [f"{a['prenom']} {a['nom']}" for a in agents_chefs]
            sel_chef = st.selectbox("Agent chef (N+1)", chef_names)

        if st.button("✅ Créer l'agent", use_container_width=True):
            if not nom or not prenom or not mail or not mdp:
                st.error("Champs obligatoires manquants.")
            else:
                id_service_new = None
                if sel_service != "— Aucun —":
                    idx = service_names.index(sel_service) - 1
                    id_service_new = services[idx]["id_service"]
                id_chef_new = None
                if sel_chef != "— Aucun —":
                    idx = chef_names.index(sel_chef) - 1
                    id_chef_new = agents_chefs[idx]["id_agent"]
                try:
                    execute_query("""
                        INSERT INTO Agent (nom, prenom, niveau_hierarchique, mail,
                                          numero_telephone, est_directeur, id_service,
                                          id_agent_chef, mot_de_passe)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (nom.upper(), prenom, niveau_new, mail,
                          telephone, 1 if est_dir else 0,
                          id_service_new, id_chef_new, hash_password(mdp)))
                    st.success(f"✅ Agent {prenom} {nom} créé avec succès !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ============================================================
# GESTION SERVICES
# ============================================================
def page_services():
   
    render_header()
    st.markdown("## 🏢 Gestion des Services")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    # Formulaire d'ajout
    with st.expander("➕ Créer un nouveau service"):
        with st.form("form_service"):
            nom = st.text_input("Nom du service")
            desc = st.text_area("Description")
            if st.form_submit_button("Enregistrer"):
                if nom:
                    execute_query("INSERT INTO Service (nom_service, description) VALUES (?,?)", (nom, desc))
                    st.success("Service créé !")
                    st.rerun()

    # Liste des services avec bouton de suppression
    services = fetch_all("SELECT * FROM Service")
    
    if not services:
        st.info("Aucun service créé pour le moment.")
    else:
        for svc in services:
            with st.container():
                # Affichage du design orange
                st.markdown(f"""
                <div class="nexus-card">
                    <div class="nexus-card-title">🏢 {svc['nom_service']} (ID: {svc['id_service']})</div>
                    <div class="nexus-card-sub">{svc['description'] if svc['description'] else 'Aucune description'}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # LE BOUTON SUPPRIMER (Bien visible en dessous de la carte)
                if st.button(f"🗑️ Supprimer l'unité {svc['id_service']}", key=f"btn_del_{svc['id_service']}"):
                    try:
                        execute_query("DELETE FROM Service WHERE id_service = ?", (svc['id_service'],))
                        st.success(f"Service {svc['nom_service']} supprimé !")
                        st.rerun()
                    except:
                        st.error("Action impossible : des agents sont encore liés à ce service.")
                st.markdown("<br>", unsafe_allow_html=True)
# ============================================================
# GESTION ACTIVITÉS
# ============================================================
def page_activites():
    render_header()
    agent = st.session_state.agent
    niveau = agent["niveau_hierarchique"]
    st.markdown("## 📋 Gestion des Activités")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Liste", "➕ Nouvelle activité"])

    with tab1:
        activites = fetch_all("""
            SELECT a.*, s.nom_service
            FROM Activite a JOIN Service s ON a.id_service=s.id_service
            ORDER BY a.id_activite DESC
        """)
        for act in activites:
            with st.expander(f"📋 {act['nom_activite']} — {act['statut'].upper()}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Type :** {act['type_activite']}")
                    st.markdown(f"**Service :** {act['nom_service']}")
                    st.markdown(f"**Début :** {act['date_debut']}")
                    st.markdown(f"**Fin :** {act['date_fin']}")
                with c2:
                    st.markdown(f"**Statut :** {act['statut']}")
                    # Participants
                    participants = fetch_all("""
                        SELECT ag.prenom || ' ' || ag.nom AS nom
                        FROM PARTICIPATION p JOIN Agent ag ON p.id_agent=ag.id_agent
                        WHERE p.id_activite=?
                    """, (act["id_activite"],))
                    if participants:
                        st.markdown(f"**Participants :** {', '.join([p['nom'] for p in participants])}")

                if niveau in ("PDG", "Directeur General"):
                    new_s = st.selectbox("Changer statut", ["planifiee", "en cours", "terminee", "annulee"],
                                         index=["planifiee", "en cours", "terminee", "annulee"].index(act["statut"]),
                                         key=f"act_s_{act['id_activite']}")
                    if st.button("💾 Sauvegarder", key=f"act_sv_{act['id_activite']}"):
                        execute_query("UPDATE Activite SET statut=? WHERE id_activite=?", (new_s, act["id_activite"]))
                        st.success("Mis à jour.")
                        st.rerun()

    with tab2:
        if niveau not in ("PDG", "Directeur General"):
            st.warning("Seuls le PDG et le Directeur Général peuvent créer des activités.")
            return

        st.markdown("### ➕ Créer une activité")
        services = fetch_all("SELECT * FROM Service ORDER BY nom_service")
        if not services:
            st.warning("Aucun service disponible. Créez d'abord un service.")
            return

        nom_act   = st.text_input("Nom de l'activité *")
        type_act  = st.text_input("Type d'activité *")
        date_deb  = st.text_input("Date de début (AAAA-MM-JJ) *", placeholder="2025-01-15")
        date_fin  = st.text_input("Date de fin (AAAA-MM-JJ) *", placeholder="2025-03-30")

        # Sélection service + affichage auto du chef
        service_names = [s["nom_service"] for s in services]
        sel_svc = st.selectbox("Service *", service_names)
        idx_svc = service_names.index(sel_svc)
        id_service_sel = services[idx_svc]["id_service"]

        # Récupération automatique du chef
        chef = fetch_one("""
            SELECT prenom || ' ' || nom AS nom_chef
            FROM Agent WHERE id_service=? AND niveau_hierarchique='Chef de service' LIMIT 1
        """, (id_service_sel,))
        if chef:
            st.info(f"👤 **Chef de service automatique :** {chef['nom_chef']}")
        else:
            st.warning("⚠️ Aucun chef de service assigné à ce service.")

        # Participants
        agents_svc = fetch_all("SELECT * FROM Agent WHERE id_service=?", (id_service_sel,))
        if agents_svc:
            participants_names = st.multiselect(
                "Participants (agents du service)",
                [f"{a['prenom']} {a['nom']}" for a in agents_svc]
            )

        if st.button("✅ Créer l'activité", use_container_width=True):
            if not nom_act or not type_act or not date_deb or not date_fin:
                st.error("Champs obligatoires manquants.")
            else:
                try:
                    id_act = execute_query("""
                        INSERT INTO Activite (nom_activite, type_activite, date_debut, date_fin, id_service)
                        VALUES (?, ?, ?, ?, ?)
                    """, (nom_act, type_act, date_deb, date_fin, id_service_sel))

                    # Ajout participants
                    if agents_svc and participants_names:
                        for ag in agents_svc:
                            if f"{ag['prenom']} {ag['nom']}" in participants_names:
                                execute_query("INSERT OR IGNORE INTO PARTICIPATION (id_agent, id_activite) VALUES (?, ?)",
                                              (ag["id_agent"], id_act))

                    # Notification au chef
                    if chef:
                        chef_ag = fetch_one("""
                            SELECT id_agent FROM Agent WHERE id_service=? AND niveau_hierarchique='Chef de service' LIMIT 1
                        """, (id_service_sel,))
                        if chef_ag:
                            send_notification(
                                chef_ag["id_agent"],
                                f"Nouvelle activité assignée : {nom_act}",
                                f"Une nouvelle activité a été créée pour votre service. Veuillez organiser les tâches.",
                                id_activite=id_act
                            )
                    st.success(f"✅ Activité « {nom_act} » créée avec succès !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ============================================================
# GESTION TÂCHES
# ============================================================
def page_taches():
    render_header()
    agent = st.session_state.agent
    niveau = agent["niveau_hierarchique"]
    id_agent = agent["id_agent"]
    id_service = agent.get("id_service")

    st.markdown("## 🗂️ Gestion des Tâches")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    if niveau == "Operant":
        # Opérant : voir ses tâches et changer statut
        st.markdown("### 📦 Mes Tâches")
        taches = fetch_all("""
            SELECT t.*, a.nom_activite
            FROM Tache t JOIN Activite a ON t.id_activite=a.id_activite
            WHERE t.id_agent_effectue=?
            ORDER BY t.id_tache DESC
        """, (id_agent,))

        if not taches:
            st.info("Aucune tâche assignée pour l'instant.")
            return

        for t in taches:
            with st.expander(f"🗂️ {t['nom_tache']} — {statut_badge(t['statut'])}", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Activité :** {t['nom_activite']}")
                    st.markdown(f"**Description :** {t['description'] or '—'}")
                    st.markdown(f"**Priorité :** {t['priorite']}")
                    st.markdown(f"**Début prévu :** {t['date_debut_prevue']}")
                    st.markdown(f"**Fin prévue :** {t['date_fin_prevue']}")
                with c2:
                    st.markdown(f"**Statut actuel :** {t['statut']}")
                    new_s = st.selectbox("Changer statut",
                                         ["non demarree", "en cours", "terminee", "annulee"],
                                         index=["non demarree", "en cours", "terminee", "annulee"].index(t["statut"]),
                                         key=f"ts_{t['id_tache']}")
                    d_r = st.text_input("Date début réelle (AAAA-MM-JJ)", value=t["date_debut_reelle"] or "", key=f"dr_{t['id_tache']}")
                    f_r = st.text_input("Date fin réelle (AAAA-MM-JJ)", value=t["date_fin_reelle"] or "", key=f"fr_{t['id_tache']}")

                if st.button("💾 Mettre à jour", key=f"tu_{t['id_tache']}"):
                    execute_query("""
                        UPDATE Tache SET statut=?, date_debut_reelle=?, date_fin_reelle=?
                        WHERE id_tache=?
                    """, (new_s, d_r or None, f_r or None, t["id_tache"]))
                    st.success("Tâche mise à jour.")
                    st.rerun()
        return

    # Chef de service / DG / PDG : créer et assigner
    tab1, tab2 = st.tabs(["📋 Liste des tâches", "➕ Nouvelle tâche"])

    with tab1:
        if niveau == "Chef de service":
            taches = fetch_all("""
                SELECT t.*, a.nom_activite,
                       ag.prenom || ' ' || ag.nom AS agent_nom
                FROM Tache t
                JOIN Activite a ON t.id_activite=a.id_activite
                JOIN Agent ag ON t.id_agent_effectue=ag.id_agent
                WHERE a.id_service=?
                ORDER BY t.id_tache DESC
            """, (id_service,))
        else:
            taches = fetch_all("""
                SELECT t.*, a.nom_activite,
                       ag.prenom || ' ' || ag.nom AS agent_nom
                FROM Tache t
                JOIN Activite a ON t.id_activite=a.id_activite
                JOIN Agent ag ON t.id_agent_effectue=ag.id_agent
                ORDER BY t.id_tache DESC
            """)

        if not taches:
            st.info("Aucune tâche trouvée.")
        for t in taches:
            st.markdown(f"""
            <div class="nexus-card">
                <div class="nexus-card-title">🗂️ {t['nom_tache']}</div>
                <div class="nexus-card-sub">
                    📋 {t['nom_activite']} &nbsp;|&nbsp;
                    👤 {t['agent_nom']} &nbsp;|&nbsp;
                    Priorité : {statut_badge(t['priorite'])} &nbsp;|&nbsp;
                    {statut_badge(t['statut'])}
                </div>
                <div class="nexus-card-sub">📅 {t['date_debut_prevue']} → {t['date_fin_prevue']}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### ➕ Créer une tâche")

        # Activités filtrées selon le niveau
        if niveau == "Chef de service":
            activites = fetch_all("SELECT * FROM Activite WHERE id_service=? ORDER BY nom_activite", (id_service,))
            # Subordonnés directs = Opérants du service
            operants = fetch_all("""
                SELECT * FROM Agent WHERE id_service=? AND niveau_hierarchique='Operant' AND statut='actif'
            """, (id_service,))
        else:
            activites = fetch_all("SELECT * FROM Activite ORDER BY nom_activite")
            operants = fetch_all("SELECT * FROM Agent WHERE niveau_hierarchique='Operant' AND statut='actif'")

        if not activites:
            st.warning("Aucune activité disponible.")
            return
        if not operants:
            st.warning("Aucun opérant disponible.")
            return

        nom_t = st.text_input("Nom de la tâche *")
        desc_t = st.text_area("Description")
        date_dp = st.text_input("Date début prévue (AAAA-MM-JJ) *", placeholder="2025-02-01")
        date_fp = st.text_input("Date fin prévue (AAAA-MM-JJ) *", placeholder="2025-02-28")
        priorite = st.selectbox("Priorité", ["faible", "moyenne", "haute"])

        act_names = [a["nom_activite"] for a in activites]
        sel_act = st.selectbox("Activité *", act_names)
        id_act_sel = activites[act_names.index(sel_act)]["id_activite"]

        op_names = [f"{o['prenom']} {o['nom']}" for o in operants]
        sel_op = st.selectbox("Assigner à (Opérant) *", op_names)
        id_op_sel = operants[op_names.index(sel_op)]["id_agent"]

        if st.button("✅ Créer la tâche", use_container_width=True):
            if not nom_t or not date_dp or not date_fp:
                st.error("Champs obligatoires manquants.")
            else:
                try:
                    id_tache = execute_query("""
                        INSERT INTO Tache (nom_tache, description, date_debut_prevue, date_fin_prevue,
                                          priorite, id_activite, id_agent_assigne, id_agent_effectue)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (nom_t, desc_t, date_dp, date_fp, priorite, id_act_sel, id_agent, id_op_sel))

                    # Historique
                    execute_query("""
                        INSERT INTO HISTORIQUE (date_historique, type_changement, motif, id_tache)
                        VALUES (?, 'affectation', 'Affectation initiale', ?)
                    """, (date.today().isoformat(), id_tache))

                    # Notification à l'opérant
                    op = operants[op_names.index(sel_op)]
                    send_notification(
                        id_op_sel,
                        f"Nouvelle tâche assignée : {nom_t}",
                        f"Vous avez été assigné à la tâche « {nom_t} » (priorité : {priorite}). Veuillez consulter les détails.",
                        id_activite=id_act_sel,
                        id_tache=id_tache
                    )

                    st.success(f"✅ Tâche « {nom_t} » créée et {op['prenom']} {op['nom']} notifié !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ============================================================
# OPÉRATIONS — Navigation par clic
# ============================================================
def page_operations():
    render_header()
    st.markdown("## 📊 Opérations — Vue par Service")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    # Navigation breadcrumb
    if st.session_state.ops_agent_id:
        if st.button("← Retour à la liste des opérants"):
            st.session_state.ops_agent_id = None
            st.rerun()
        _show_agent_detail(st.session_state.ops_agent_id)
        return

    if st.session_state.ops_service_id:
        if st.button("← Retour aux services"):
            st.session_state.ops_service_id = None
            st.rerun()
        _show_service_agents(st.session_state.ops_service_id)
        return

    # Liste des services
    services = fetch_all("SELECT * FROM Service ORDER BY nom_service")
    if not services:
        st.info("Aucun service enregistré.")
        return

    st.markdown("### 🏢 Sélectionnez un service")
    cols = st.columns(3)
    for i, svc in enumerate(services):
        nb_agents = fetch_one("SELECT COUNT(*) FROM Agent WHERE id_service=?", (svc["id_service"],))[0]
        nb_act    = fetch_one("SELECT COUNT(*) FROM Activite WHERE id_service=?", (svc["id_service"],))[0]
        with cols[i % 3]:
            st.markdown(f"""
            <div class="nexus-card" style="cursor:pointer;">
                <div class="nexus-card-title">🏢 {svc['nom_service']}</div>
                <div class="nexus-card-sub">👥 {nb_agents} agents &nbsp;|&nbsp; 📋 {nb_act} activités</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Voir {svc['nom_service']}", key=f"svc_{svc['id_service']}"):
                st.session_state.ops_service_id = svc["id_service"]
                st.rerun()

def _show_service_agents(id_service):
    svc = fetch_one("SELECT * FROM Service WHERE id_service=?", (id_service,))
    st.markdown(f"### 👥 Opérants du service : {svc['nom_service']}")

    agents = fetch_all("""
        SELECT * FROM Agent WHERE id_service=? AND niveau_hierarchique='Operant'
        ORDER BY nom
    """, (id_service,))

    if not agents:
        st.info("Aucun opérant dans ce service.")
        return

    cols = st.columns(3)
    for i, ag in enumerate(agents):
        total = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=?", (ag["id_agent"],))[0]
        done  = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=? AND statut='terminee'", (ag["id_agent"],))[0]
        with cols[i % 3]:
            st.markdown(f"""
            <div class="nexus-card">
                <div class="nexus-card-title">👤 {ag['prenom']} {ag['nom']}</div>
                <div class="nexus-card-sub">
                    📦 {total} tâches &nbsp;|&nbsp; ✅ {done} terminées<br>
                    {statut_badge(ag['statut'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Voir le profil", key=f"ag_ops_{ag['id_agent']}"):
                st.session_state.ops_agent_id = ag["id_agent"]
                st.rerun()

def _show_agent_detail(id_agent):
    ag = fetch_one("SELECT * FROM Agent WHERE id_agent=?", (id_agent,))
    svc = fetch_one("SELECT nom_service FROM Service WHERE id_service=?", (ag["id_service"],)) if ag["id_service"] else None

    st.markdown(f"### 👤 Profil : {ag['prenom']} {ag['nom']}")
    c1, c2, c3 = st.columns(3)

    total  = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=?", (id_agent,))[0]
    done   = fetch_one("SELECT COUNT(*) FROM Tache WHERE id_agent_effectue=? AND statut='terminee'", (id_agent,))[0]
    retard = fetch_one("""
        SELECT COUNT(*) FROM Tache
        WHERE id_agent_effectue=? AND statut NOT IN ('terminee','annulee')
        AND date_fin_prevue < ?
    """, (id_agent, date.today().isoformat()))[0]

    with c1: st.metric("📦 Total tâches", total)
    with c2: st.metric("✅ Terminées", done)
    with c3: st.metric("⏰ En retard", retard)

    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    # Infos
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Email :** {ag['mail']}")
        st.markdown(f"**Tél :** {ag['numero_telephone'] or '—'}")
        st.markdown(f"**Service :** {svc['nom_service'] if svc else '—'}")
    with col2:
        st.markdown(f"**Statut :** {ag['statut']}")
        st.markdown(f"**Niveau :** {ag['niveau_hierarchique']}")

    st.markdown("### 🗂️ Tâches en cours")
    taches = fetch_all("""
        SELECT t.*, a.nom_activite FROM Tache t
        JOIN Activite a ON t.id_activite=a.id_activite
        WHERE t.id_agent_effectue=?
        ORDER BY t.statut, t.date_fin_prevue
    """, (id_agent,))

    if not taches:
        st.info("Aucune tâche.")
    for t in taches:
        st.markdown(f"""
        <div class="nexus-card">
            <div class="nexus-card-title">{t['nom_tache']}</div>
            <div class="nexus-card-sub">
                📋 {t['nom_activite']} &nbsp;|&nbsp;
                Priorité : {statut_badge(t['priorite'])} &nbsp;|&nbsp;
                {statut_badge(t['statut'])}
            </div>
            <div class="nexus-card-sub">📅 {t['date_debut_prevue']} → {t['date_fin_prevue']}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# NOTIFICATIONS
# ============================================================
def page_notifications():
    render_header()
    agent = st.session_state.agent
    id_agent = agent["id_agent"]
    st.markdown("## 🔔 Notifications")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📬 Non lues", "📂 Toutes"])

    with tab1:
        notifs = fetch_all("""
            SELECT * FROM NOTIFICATION WHERE id_agent=? AND statut='envoyee'
            ORDER BY date_envoie DESC
        """, (id_agent,))
        if not notifs:
            st.success("✅ Aucune notification en attente.")
        for n in notifs:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="notif-item">
                    <div class="notif-title">🔔 {n['titre']}</div>
                    <div class="notif-desc">{n['description']}</div>
                    <div class="notif-date">{n['date_envoie']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✔ Lu", key=f"lu2_{n['id_notification']}"):
                    execute_query("UPDATE NOTIFICATION SET statut='lue' WHERE id_notification=?", (n["id_notification"],))
                    st.rerun()

    with tab2:
        notifs_all = fetch_all("""
            SELECT * FROM NOTIFICATION WHERE id_agent=?
            ORDER BY date_envoie DESC
        """, (id_agent,))
        for n in notifs_all:
            opacity = "0.6" if n["statut"] != "envoyee" else "1"
            st.markdown(f"""
            <div class="notif-item" style="opacity:{opacity}">
                <div class="notif-title">🔔 {n['titre']}
                    <span style="font-size:0.75rem;color:#999;font-weight:400;"> — {n['statut']}</span>
                </div>
                <div class="notif-desc">{n['description']}</div>
                <div class="notif-date">{n['date_envoie']}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# BOÎTE À IDÉES
# ============================================================
def page_boite_idees():
    render_header()
    agent = st.session_state.agent
    id_agent = agent["id_agent"]
    niveau = agent["niveau_hierarchique"]
    st.markdown("## 💡 Boîte à Idées")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Idées soumises", "➕ Soumettre une idée"])

    with tab1:
        if niveau in ("PDG", "Directeur General"):
            idees = fetch_all("""
                SELECT i.*, ag.prenom || ' ' || ag.nom AS auteur
                FROM Boite_idee i JOIN Agent ag ON i.id_agent=ag.id_agent
                ORDER BY i.id_idee DESC
            """)
        else:
            idees = fetch_all("""
                SELECT i.*, ag.prenom || ' ' || ag.nom AS auteur
                FROM Boite_idee i JOIN Agent ag ON i.id_agent=ag.id_agent
                WHERE i.id_agent=?
                ORDER BY i.id_idee DESC
            """, (id_agent,))

        for idee in idees:
            with st.expander(f"💡 {idee['titre']} — {idee['statut'].upper()}"):
                st.markdown(f"**Auteur :** {idee['auteur']}")
                st.markdown(f"**Domaine :** {idee['domaine'] or '—'}")
                st.markdown(f"**Contenu :** {idee['contenu']}")
                if niveau in ("PDG", "Directeur General"):
                    new_s = st.selectbox("Statut", ["soumise", "en etude", "acceptee", "rejetee"],
                                         index=["soumise", "en etude", "acceptee", "rejetee"].index(idee["statut"]),
                                         key=f"idee_s_{idee['id_idee']}")
                    if st.button("💾 Mettre à jour", key=f"idee_u_{idee['id_idee']}"):
                        execute_query("UPDATE Boite_idee SET statut=? WHERE id_idee=?", (new_s, idee["id_idee"]))
                        st.success("Statut mis à jour.")
                        st.rerun()

    with tab2:
        titre_i = st.text_input("Titre *")
        domaine = st.text_input("Domaine")
        contenu_i = st.text_area("Contenu de l'idée *")
        if st.button("✅ Soumettre l'idée", use_container_width=True):
            if not titre_i or not contenu_i:
                st.error("Titre et contenu obligatoires.")
            else:
                execute_query("INSERT INTO Boite_idee (titre, contenu, domaine, id_agent) VALUES (?, ?, ?, ?)",
                              (titre_i, contenu_i, domaine, id_agent))
                st.success("Idée soumise !")
                st.rerun()

# ============================================================
# SIGNALEMENTS
# ============================================================
def page_signalements():
    render_header()
    agent = st.session_state.agent
    id_agent = agent["id_agent"]
    niveau = agent["niveau_hierarchique"]
    st.markdown("## ⚠️ Signalements")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Liste", "➕ Nouveau signalement"])

    with tab1:
        if niveau in ("PDG", "Directeur General"):
            signalements = fetch_all("""
                SELECT s.*, ag.prenom || ' ' || ag.nom AS auteur
                FROM Signalement s JOIN Agent ag ON s.id_agent=ag.id_agent
                ORDER BY s.id_signalement DESC
            """)
        else:
            signalements = fetch_all("""
                SELECT s.*, ag.prenom || ' ' || ag.nom AS auteur
                FROM Signalement s JOIN Agent ag ON s.id_agent=ag.id_agent
                WHERE s.id_agent=?
                ORDER BY s.id_signalement DESC
            """, (id_agent,))

        for sg in signalements:
            urg_col = {"faible": "#2E7D32", "moyen": "#E65100", "urgent": "#C62828"}.get(sg["niveau_urgence"], "#666")
            st.markdown(f"""
            <div class="nexus-card">
                <div class="nexus-card-title">⚠️ {sg['titre']}
                    <span style="color:{urg_col};font-size:0.85rem;"> [{sg['niveau_urgence'].upper()}]</span>
                </div>
                <div class="nexus-card-sub">{sg['description']}</div>
                <div class="nexus-card-sub">
                    👤 {sg['auteur']} &nbsp;|&nbsp; 📅 {sg['date_signalement']} &nbsp;|&nbsp; {statut_badge(sg['statut'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if niveau in ("PDG", "Directeur General"):
                new_s = st.selectbox("Statut", ["ouvert", "en traitement", "resolu", "ferme"],
                                     index=["ouvert", "en traitement", "resolu", "ferme"].index(sg["statut"]),
                                     key=f"sg_s_{sg['id_signalement']}")
                if st.button("💾 Mettre à jour", key=f"sg_u_{sg['id_signalement']}"):
                    execute_query("UPDATE Signalement SET statut=? WHERE id_signalement=?", (new_s, sg["id_signalement"]))
                    st.success("Mis à jour.")
                    st.rerun()

    with tab2:
        titre_sg = st.text_input("Titre *")
        desc_sg   = st.text_area("Description *")
        urgence   = st.selectbox("Niveau d'urgence *", ["faible", "moyen", "urgent"])
        if st.button("✅ Signaler", use_container_width=True):
            if not titre_sg or not desc_sg:
                st.error("Titre et description obligatoires.")
            else:
                execute_query("INSERT INTO Signalement (titre, description, niveau_urgence, id_agent) VALUES (?, ?, ?, ?)",
                              (titre_sg, desc_sg, urgence, id_agent))
                st.success("Signalement créé !")
                st.rerun()

# ============================================================
# AVIS
# ============================================================
def page_avis():
    render_header()
    agent = st.session_state.agent
    id_agent = agent["id_agent"]
    niveau = agent["niveau_hierarchique"]
    st.markdown("## ⭐ Avis & Retours")
    st.markdown('<hr class="orange-sep">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Avis reçus", "➕ Laisser un avis"])

    with tab1:
        if niveau in ("PDG", "Directeur General"):
            avis_list = fetch_all("""
                SELECT av.*, ag.prenom || ' ' || ag.nom AS auteur
                FROM AVIS av JOIN Agent ag ON av.id_agent=ag.id_agent
                ORDER BY av.id_avis DESC
            """)
        else:
            avis_list = fetch_all("""
                SELECT av.*, ag.prenom || ' ' || ag.nom AS auteur
                FROM AVIS av JOIN Agent ag ON av.id_agent=ag.id_agent
                WHERE av.id_agent=?
                ORDER BY av.id_avis DESC
            """, (id_agent,))

        for av in avis_list:
            stars = "⭐" * (av["note"] or 0)
            st.markdown(f"""
            <div class="nexus-card">
                <div class="nexus-card-title">{av['titre']} {stars}</div>
                <div class="nexus-card-sub">👤 {av['auteur']} &nbsp;|&nbsp; 📅 {av['date_avis']}</div>
                <div class="nexus-card-sub" style="margin-top:6px;">{av['contenu']}</div>
                {f"<div class='nexus-card-sub'>📌 Fonctionnalité : {av['fonctionnalite_concernee']}</div>" if av['fonctionnalite_concernee'] else ""}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        titre_av = st.text_input("Titre *")
        contenu_av = st.text_area("Contenu *")
        note = st.slider("Note", 1, 5, 3)
        fonct = st.text_input("Fonctionnalité concernée")
        if st.button("✅ Soumettre l'avis", use_container_width=True):
            if not titre_av or not contenu_av:
                st.error("Titre et contenu obligatoires.")
            else:
                execute_query("INSERT INTO AVIS (titre, contenu, note, fonctionnalite_concernee, id_agent) VALUES (?, ?, ?, ?, ?)",
                              (titre_av, contenu_av, note, fonct or None, id_agent))
                st.success("Avis soumis !")
                st.rerun()

# ============================================================
# ROUTEUR PRINCIPAL
# ============================================================
def main():
    if not st.session_state.authenticated:
        page_login()
        return

    agent = st.session_state.agent
    niveau = agent["niveau_hierarchique"]
    menu_items = get_menu_items(niveau)

    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:1.5rem 0 1rem;">
            <div style="font-family:'Barlow Condensed',sans-serif; font-weight:900;
                        font-size:2.2rem; color:#FF7900; letter-spacing:3px;">NEXUS</div>
            <div style="color:#AAA; font-size:0.75rem; letter-spacing:1px;">SYSTÈME RAMA</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#222; border-radius:6px; padding:0.8rem; margin-bottom:1rem; border-left:3px solid #FF7900;">
            <div style="font-weight:700; color:#FF7900; font-size:0.95rem;">
                {agent['prenom']} {agent['nom']}
            </div>
            <div style="color:#AAA; font-size:0.8rem;">{niveau}</div>
        </div>
        """, unsafe_allow_html=True)

        selected = st.radio("Navigation", menu_items, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.agent = None
            st.session_state.ops_service_id = None
            st.session_state.ops_agent_id = None
            st.rerun()

    # Routing
    page_map = {
        "🏠 Tableau de Bord": page_dashboard,
        "👥 Gestion Agents":  page_agents,
        "🏢 Services":        page_services,
        "📋 Activités":       page_activites,
        "🗂️ Tâches":          page_taches,
        "🗂️ Mes Tâches":      page_taches,
        "📊 Opérations":      page_operations,
        "🔔 Notifications":   page_notifications,
        "💡 Boîte à Idées":   page_boite_idees,
        "⚠️ Signalements":    page_signalements,
        "⭐ Avis":            page_avis,
    }

    page_fn = page_map.get(selected, page_dashboard)
    page_fn()

if __name__ == "__main__":
    main()
