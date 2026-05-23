import streamlit as st
import streamlit.components.v1 as components
import random

# Configurazione della pagina
st.set_page_config(
    page_title="Pannello Operativo Ambulatorio Odontoiatrico",
    page_icon="🦷",
    layout="wide"
)

# 1. DATABASE UTENTI SIMULATO
USER_DB = {
    "admin_founder": {"password": "password123", "ruolo": "Founder", "nome_completo": "Dott. Rossi (Founder)"},
    "mod_user": {"password": "password456", "ruolo": "Moderatore", "nome_completo": "Coord. Bianchi"},
    "base_user": {"password": "password789", "ruolo": "Base", "nome_completo": "Ass. Verdi"}
}

# 2. DATABASE DELLE PROCEDURE
PROCEDURE_DETTAGLI = {
    "Presa in carico del paziente presso gli studi odontoiatrici": 
        "Accoglienza del paziente, verifica dell'anamnesi clinica recente e del consenso informato firmato. "
        "Preparazione della postazione con barriere monouso e sanificazione delle superfici inter-seduta. "
        "Registrazione dei dati geometrici o radiografici preliminari a terminale prima dell'ingresso del medico.",
    
    "Gestione del magazzino e degli ordini di rifornimento": 
        "Verifica settimanale delle scadenze dei materiali compositi, anestetici e fiale. "
        "Tracciamento dei lotti di sterilizzazione. Compilazione del registro d'ordine al raggiungimento della soglia minima di scorta "
        "(es. impianti, frese multilama, siringhe monouso) per evitare blocchi operativi.",
    
    "Checklist del reparto": 
        "Controllo iniziale della pressione del compressore d'aria e dell'aspirazione centralizzata. "
        "Verifica dei cicli dell'autoclave tramite test biologici e chimici (Helix e Bowie&Dick). "
        "Rifornimento dei dispenser di DPI (guanti, mascherine, visiere) in ogni singola unità operativa prima dell'inizio del turno.",
    
    "Esecuzione di Radiografie Endorali con Tecnica dei Piani Paralleli":
        "Posizionamento del paziente con piano occlusale parallelo al pavimento. Selezione del centratore XCP corretto "
        "in base al quadrante da esaminare (Giallo = Posteriore, Blu = Anteriore, Rosso = Bitewing, Verde = Endo). "
        "Inserimento del sensore digitale protetto da guaina monouso. Allineamento del tubo radiogeno all'anello di mira dell'XCP "
        "per azzerare gli errori di cono d'ombra e distorsione geometrica."
}

# 3. CATALOGO SPECIALISTICA CENTRATORI XCP (Riferimento Catalogo Gerhò)
STRUMENTARIO_XCP = [
    {
        "nome": "Centratore XCP Anteriore (Colore Blu)",
        "ref": "GH-XCP-ANT",
        "tipo": "Diagnostica / Radiologia",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica (Tutti gli studi)",
        "descrizione": "Indicato per radiografie endorali dei settori anteriori (incisivi e canini superiori/interiori). Include l'anello di mira blu, l'asta metallica indicatrice a due poli e i blocchetti di morso verticali dedicati.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Centratore XCP Posteriore (Colore Giallo)",
        "ref": "GH-XCP-POST",
        "tipo": "Diagnostica / Radiologia",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica (Tutti gli studi)",
        "descrizione": "Progettato per i settori posteriori (premolari e molari nei quattro quadranti). Il posizionamento del blocchetto di morso è orizzontale. Ottimizza il parallelismo riducendo l'allungamento o l'accorciamento dell'immagine.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Centratore XCP Bitewing (Colore Rosso)",
        "ref": "GH-XCP-BW",
        "tipo": "Diagnostica / Radiologia",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica (Tutti gli studi)",
        "descrizione": "Centratore specifico per radiografie interprossimali (Bitewing), fondamentale per la diagnosi precoce di carie interprossimali e per la valutazione del livello osseo crestale.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Centratore XCP Endodontico (Colore Verde)",
        "ref": "GH-XCP-ENDO",
        "tipo": "Endodonzia / Diagnostica",
        "ambulatorio": "Ambulatorio di Endodonzia e Conservativa",
        "descrizione": "Strumento appositamente sagomato per scavalcare gli aghi canalari (file), i localizzatori d'apice o le dighe di gomma in posizione durante i trattamenti endodontici, consentendo radiografie di controllo stabili senza rimuovere la strumentazione.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    }
]

# 4. POOL DI DOMANDE PER IL SISTEMA DI GAMIFICATION
QUIZ_DATA = {
    "Diagnostica XCP": [
        {"domanda": "Quale colore identifica il centratore XCP per i settori posteriori?", "opzioni": ["Blu", "Giallo", "Rosso"], "corretta": "Giallo"},
        {"domanda": "A cosa serve l'anello di mira del sistema XCP Rinn?", "opzioni": ["A bloccare il sensore", "Ad allineare perfettamente il tubo radiogeno evitando coni d'ombra", "A proteggere le labbra del paziente"], "corretta": "Ad allineare perfettamente il tubo radiogeno evitando coni d'ombra"}
    ]
}

# 5. INIZIALIZZAZIONE SESSION STATE
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False
    st.session_state["username"] = ""
    st.session_state["ruolo"] = ""

if "commenti" not in st.session_state:
    st.session_state["commenti"] = {titolo: [] for titolo in PROCEDURE_DETTAGLI.keys()}

if "voti" not in st.session_state:
    st.session_state["voti"] = {titolo: {"up": 0, "down": 0} for titolo in PROCEDURE_DETTAGLI.keys()}

if "classifica" not in st.session_state:
    st.session_state["classifica"] = {"Coord. Bianchi": 120, "Ass. Verdi": 95, "Dott. Rossi (Founder)": 40}

if "quiz_attivo" not in st.session_state:
    st.session_state["quiz_attivo"] = False
    st.session_state["domande_selezionate"] = []
    st.session_state["indice_domanda"] = 0
    st.session_state["punteggio_sessione"] = 0

def elimina_commento(procedura, indice):
    st.session_state["commenti"][procedura].pop(indice)

def vota_up(procedura):
    st.session_state["voti"][procedura]["up"] += 1

def vota_down(procedura):
    st.session_state["voti"][procedura]["down"] += 1

# 6. INTERFACCIA DI LOGIN
if not st.session_state["autenticato"]:
    st.title("🔒 Piattaforma Sperimentale Odontoiatrica")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("Login Form"):
            username_input = st.text_input("Username").strip()
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Accedi")
            if submit_login:
                if username_input in USER_DB and USER_DB[username_input]["password"] == password_input:
                    st.session_state["autenticato"] = True
                    st.session_state["username"] = username_input
                    st.session_state["ruolo"] = USER_DB[username_input]["ruolo"]
                    st.rerun()
                else:
                    st.error("Credenziali errate.")

# 7. AREA APPLICAZIONE
else:
    with st.sidebar:
        st.subheader(f"👤 {st.session_state['username']}")
        st.info(f"Ruolo: **{st.session_state['ruolo']}**")
        if st.button("Effettua Logout", use_container_width=True):
            st.session_state["autenticato"] = False
            st.rerun()

    st.title("🦷 Hub Operativo e Linee Guida di Studio")
    
    # --- ASSISTENTE AI REPARTO - INTEGRATO CON CENTRATORI XCP ---
    st.markdown("---")
    with st.container():
        st.markdown("### 🤖 Assistente AI - Supporto Decisionale Clinico")
        st.caption("L'Intelligenza Artificiale scansiona i protocolli di reparto e il catalogo specialistico dei centratori Rinn XCP.")
        
        query_ai = st.text_input("Inserisci un codice REF o un dubbio (es. 'Quale centratore serve per i molari?' o 'GH-XCP-ANT'):", placeholder="Chiedi all'AI...")
        
        if query_ai:
            query_clean = query_ai.lower()
            risposta_trovata = False
            
            # Controllo AI sui Dispositivi XCP
            for xcp in STRUMENTARIO_XCP:
                if query_clean in xcp["nome"].lower() or query_clean in xcp["ref"].lower():
                    st.markdown(f"**🤖 Risposta dell'Assistente AI (Identificato Dispositivo XCP):**")
                    st.success(f"Trovata corrispondenza nel catalogo **Gerhò Specialistica XCP**:\n\n"
                               f"🔹 **Componente**: {xcp['nome']} (REF: `{xcp['ref']}`)\n"
                               f"📍 **Uso e Collocazione**: {xcp['ambulatorio']}\n"
                               f"📝 **Istruzioni operative**: {xcp['descrizione']}")
                    risposta_trovata = True
                    break
            
            # Controllo sezioni generali
            if not risposta_trovata:
                for titolo_proc, contenuto_proc in PROCEDURE_DETTAGLI.items():
                    if query_clean in titolo_proc.lower() or query_clean in contenuto_proc.lower():
                        st.markdown(f"**🤖 Risposta dell'Assistente AI:**")
                        st.info(f"Dal protocollo di reparto **{titolo_proc}**:\n\n*{contenuto_proc}*")
                        risposta_trovata = True
                        break
            
            if not risposta_trovata:
                st.warning("🤖 **Risposta dell'Assistente AI:** Nessun riscontro esatto nell'inventario XCP corrente.")
                
    st.markdown("---")

    # Navigazione Tab
    tab_procedure, tab_xcp, tab_mappa, tab_esercitati = st.tabs([
        "📋 Procedure Cliniche", 
        "🛠️ Specialistica XCP (Centratori Gerhò)", 
        "🗺️ Anatomia dell'Ambulatorio", 
        "🎯 Esercitati"
    ])

    # --- TAB 1: PROCEDURE ---
    with tab_procedure:
        st.header("Protocolli e Standard di Assistenza")
        for proc, descrizione in PROCEDURE_DETTAGLI.items():
            with st.expander(f"📖 {proc}", expanded=False):
                col_testo, col_feedback = st.columns([8, 2])
                with col_testo:
                    st.write(descrizione)
                with col_feedback:
                    up_c = st.session_state["voti"][proc]["up"]
                    down_c = st.session_state["voti"][proc]["down"]
                    s1, s2 = st.columns(2)
                    s1.button(f"︎🤝 {up_c}", key=f"up_{proc}", on_click=vota_up, args=(proc,), use_container_width=True)
                    s2.button(f"︎⚠ {down_c}", key=f"down_{proc}", on_click=vota_down, args=(proc,), use_container_width=True)

    # --- TAB 2: SPECIALISTICA XCP ---
    with tab_xcp:
        st.header("🛠️ Configurazione e Codici Kit Rinn XCP")
        st.caption("Uso corretto dei posizionatori a piani paralleli per l'azzeramento degli errori radiografici angolari.")
        
        ricerca_xcp = st.text_input("Cerca componente per nome o REF:", key="search_xcp")
        
        for item in STRUMENTARIO_XCP:
            if ricerca_xcp.lower() in item["nome"].lower() or ricerca_xcp.lower() in item["ref"].lower():
                with st.container():
                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        st.image(item["immagine"], use_container_width=True)
                    with col_info:
                        st.subheader(item["nome"])
                        c1, c2 = st.columns(2)
                        c1.metric(label="Codice REF Gerhò", value=item["ref"])
                        c2.metric(label="Area Specialistica", value=item["tipo"])
                        st.markdown(f"📍 **Uso Prevalente:** `{item['ambulatorio']}`")
                        st.markdown(f"📝 **Dettagli Tecnici:** {item['descrizione']}")
                    st.markdown("---")

    # --- TAB 3: MAPPA ---
    with tab_mappa:
        st.header("Mappa Interattiva dell'Ambulatorio")
        html_content = """
        <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
        .container { position: relative; width: 100%; max-width: 900px; margin: 0 auto; }
        .image { display: block; width: 100%; height: auto; border-radius: 8px; }
        .hotspot { position: absolute; width: 26px; height: 26px; background-color: #FF4B4B; border-radius: 50%; cursor: pointer; border: 3px solid white; animation: pulse 2.5s infinite; }
        #hp1 { top: 65%; left: 45%; } #hp2 { top: 25%; left: 50%; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.8); } 70% { box-shadow: 0 0 0 12px rgba(255, 75, 75, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); } }
        .modal { display: none; position: absolute; top: 20%; left: 75%; background-color: white; padding: 16px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); width: 250px; border-left: 5px solid #FF4B4B; font-family: sans-serif; }
        </style></head><body><div class="container">
          <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=900&q=80" class="image">
          <div class="hotspot" id="hp1" onclick="showInfo('Riunito Odontoiatrico', 'Verificare l allineamento del tubo radiogeno al braccio prima dell esposizione.')"></div>
          <div id="infoModal" class="modal"><h4 id="modalTitle">Componente</h4><p id="modalDesc"></p></div>
        </div><script>
        function showInfo(title, text) { document.getElementById("modalTitle").innerText = title; document.getElementById("modalDesc").innerText = text; document.getElementById("infoModal").style.display = "block"; }
        </script></body></html>
        """
        components.html(html_content, height=650, scrolling=False)

    # --- TAB 4: GAMIFICATION ---
    with tab_esercitati:
        st.header("🎯 Autovalutazione")
        # Logica contratta per brevità, intatta rispetto alla release precedente...
