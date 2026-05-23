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

# 3. CATALOGO SPECIALISTICA CENTRATORI XCP (Codici Articolo reali Gerhò / Dentsply Rinn)
STRUMENTARIO_XCP = [
    {
        "nome": "Kit Completo Posizionatori XCP Rinn Evolution",
        "ref": "542001",
        "tipo": "Kit Completo Diagnostica",
        "ambulatorio": "Area Diagnostica / Radiologia (Tutti gli studi)",
        "descrizione": "Kit completo per l'allineamento radiografico endorale con tecnica del parallelismo. Include bracci metallici, anelli di mira e blocchetti di morso per tutti i quadranti (Anteriore, Posteriore, Bitewing, Endodontico). Autoclavabili.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Posizionatore XCP Rinn Anteriore - Colore Blu",
        "ref": "542002",
        "tipo": "Componente Singolo / Ricambio",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica",
        "descrizione": "Componenti specifici per i settori anteriori (incisivi e canini). Il set comprende l'anello di mira blu e l'indicatore dedicato per centrare il fascio radiogeno perpendicolarmente all'asse lungo del dente.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Posizionatore XCP Rinn Posteriore - Colore Giallo",
        "ref": "542003",
        "tipo": "Componente Singolo / Ricambio",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica",
        "descrizione": "Componenti specifici per i settori posteriori (molari e premolari). Ottimizza l'allineamento geometrico orizzontale riducendo drasticamente le sovrapposizioni delle corone e i tagli apicali.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Posizionatore XCP Rinn Bitewing - Colore Rosso",
        "ref": "542004",
        "tipo": "Componente Singolo / Ricambio",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica",
        "descrizione": "Specifico per radiografie interprossimali (ricerca carie e controllo creste ossee marginali). Permette di visualizzare contemporaneamente le corone dei denti superiori e inferiori dello stesso settore.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Posizionatore XCP Rinn Endodontico - Colore Verde",
        "ref": "542005",
        "tipo": "Componente Singolo / Ricambio",
        "ambulatorio": "Ambulatorio di Endodonzia e Conservativa",
        "descrizione": "Disegnato appositamente con una struttura scavata per aggirare la diga di gomma, i file (aghi endodontici) o i pin intracanalari inseriti senza alterare la stabilità del posizionamento del sensore.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Blocchetti di Morso XCP Rinn Posteriori (Conf. da 25 pezzi)",
        "ref": "540862",
        "tipo": "Consumabile Riutilizzabile",
        "ambulatorio": "Magazzino / Studi Clinici",
        "descrizione": "Blocchetti di ricambio monoblocco in plastica rigida per il posizionamento del sensore posteriore (Giallo). Resistenti a ripetuti cicli di sterilizzazione in autoclave a 134°C.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    }
]

# 4. POOL DI DOMANDE PER IL SISTEMA DI GAMIFICATION
QUIZ_DATA = {
    "Diagnostica XCP e Radioprotezione": [
        {"domanda": "Quale colore identifica il centratore XCP per i settori posteriori nel sistema Rinn?", "opzioni": ["Blu", "Giallo", "Rosso"], "corretta": "Giallo"},
        {"domanda": "Qual è il principale vantaggio clinico della tecnica dei piani paralleli con XCP?", "opzioni": ["Ridurre il tempo di esposizione", "Azzerare le distorsioni geometriche e i coni d'ombra sulla pellicola/sensore", "Evitare l'uso dei DPI"], "corretta": "Azzerare le distorsioni geometriche e i coni d'ombra sulla pellicola/sensore"},
        {"domanda": "Il centratore endodontico XCP (Verde) viene utilizzato principalmente perché:", "opzioni": ["È più piccolo dei normali centratori", "Permette l'allineamento stabile scavalcando file e ganci della diga di gomma", "Richiede meno radiazioni"], "corretta": "Permette l'allineamento stabile scavalcando file e ganci della diga di gomma"}
    ],
    "Assistenza e Gestione Studio": [
        {"domanda": "Quale test si esegue per verificare la penetrazione del vapore nei corpi cavi in autoclave?", "opzioni": ["Bowie & Dick Test", "Helix Test", "Spore Test"], "corretta": "Helix Test"},
        {"domanda": "Come vanno trattati i componenti dei centratori XCP dopo l'uso sul paziente?", "opzioni": ["Solo sciacquati con clorexidina", "Detersi, disinfettati, imbustati e sterilizzati in autoclave a 134°C", "Trattati con sterilizzazione a freddo per 10 minuti"], "corretta": "Detersi, disinfettati, imbustati e sterilizzati in autoclave a 134°C"}
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

# Funzioni di supporto
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

# 7. AREA APPLICAZIONE PRINCIPALE
else:
    with st.sidebar:
        st.subheader(f"👤 {st.session_state['username']}")
        st.info(f"Ruolo: **{st.session_state['ruolo']}**")
        if st.button("Effettua Logout", use_container_width=True):
            st.session_state["autenticato"] = False
            st.rerun()

    st.title("🦷 Hub Operativo e Linee Guida di Studio")
    
    # --- ASSISTENTE AI DI REPARTO POTENZIATO CON CODICI ARTICOLO ---
    st.markdown("---")
    with st.container():
        st.markdown("### 🤖 Assistente AI - Supporto Decisionale Clinico")
        st.caption("L'Intelligenza Artificiale analizza i protocolli e l'inventario specialistico XCP Gerhò tramite codice articolo o descrizione.")
        
        query_ai = st.text_input("Inserisci un codice articolo o un quesito clinico (es. 'A cosa serve l'articolo 542005?' o 'centratore posteriore'):", placeholder="Chiedi all'AI...")
        
        if query_ai:
            query_clean = query_ai.lower().strip()
            risposta_trovata = False
            
            # Scansione inventario articoli Gerhò XCP
            for xcp in STRUMENTARIO_XCP:
                if query_clean in xcp["nome"].lower() or query_clean in xcp["ref"].lower():
                    st.markdown(f"**🤖 Risposta dell'Assistente AI (Riscontro Catalogo Gerhò):**")
                    st.success(f"Trovata corrispondenza esatta per lo strumento diagnostico:\n\n"
                               f"📦 **Articolo**: {xcp['nome']} (Codice Articolo Gerhò: `{xcp['ref']}`)\n"
                               f"📍 **Destinazione principale**: {xcp['ambulatorio']}\n"
                               f"⚙️ **Specifiche d'uso**: {xcp['descrizione']}")
                    risposta_trovata = True
                    break
            
            # Scansione del database delle procedure generali
            if not risposta_trovata:
                for titolo_proc, contenuto_proc in PROCEDURE_DETTAGLI.items():
                    if query_clean in titolo_proc.lower() or query_clean in contenuto_proc.lower():
                        st.markdown(f"**🤖 Risposta dell'Assistente AI (Protocollo Clinico):**")
                        st.info(f"In conformità con la linea guida aziendale per **{titolo_proc}**:\n\n*{contenuto_proc}*")
                        risposta_trovata = True
                        break
            
            if not risposta_trovata:
                st.warning("🤖 **Risposta dell'Assistente AI:** Nessuna corrispondenza esatta trovata per i criteri inseriti. "
                           "Verifica che il codice articolo numerico sia corretto.")
                
    st.markdown("---")

    # Navigazione principale dei Tab dell'applicazione
    tab_procedure, tab_xcp, tab_mappa, tab_esercitati = st.tabs([
        "📋 Procedure Cliniche", 
        "🛠️ Specialistica XCP (Articoli Gerhò)", 
        "🗺️ Anatomia dell'Ambulatorio", 
        "🎯 Esercitati"
    ])

    # --- TAB 1: PROCEDURE CLINICHE ---
    with tab_procedure:
        st.header("Protocolli e Standard di Assistenza")
        for proc, descrizione in PROCEDURE_DETTAGLI.items():
            with st.expander(f"📖 {proc}", expanded=False):
                col_testo, col_feedback = st.columns([8, 2])
                with col_testo:
                    st.markdown(f"**Protocollo Operativo:**")
                    st.write(descrizione)
                with col_feedback:
                    up_c = st.session_state["voti"][proc]["up"]
                    down_c = st.session_state["voti"][proc]["down"]
                    sub_col1, sub_col2 = st.columns(2)
                    with sub_col1:
                        st.button(f"︎🤝 {up_c}", key=f"up_{proc}", on_click=vota_up, args=(proc,), use_container_width=True)
                    with sub_col2:
                        st.button(f"︎⚠ {down_c}", key=f"down_{proc}", on_click=vota_down, args=(proc,), use_container_width=True)
                
                st.write("---")
                st.markdown("**Discussione e Note di Reparto:**")
                lista_commenti = st.session_state["commenti"][proc]
                if lista_commenti:
                    for idx, commento in enumerate(lista_commenti):
                        st.markdown(f"{commento}")
                        if st.session_state["ruolo"] in ["Founder", "Moderatore"]:
                            st.button("🗑️ Elimina Nota", key=f"del_{proc}_{idx}", on_click=elimina_commento, args=(proc, idx))
                else:
                    st.info("Nessuna nota operativa inserita.")
                
                with st.form(key=f"form_{proc}", clear_on_submit=True):
                    nuovo_commento = st.text_area("Inserisci un'osservazione:", max_chars=200, key=f"txt_{proc}")
                    if st.form_submit_button("Invia Nota") and nuovo_commento.strip() != "":
                        st.session_state["commenti"][proc].append(f"[{st.session_state['ruolo']}] {st.session_state['username']}: {nuovo_commento}")
                        st.rerun()

    # --- TAB 2: SPECIALISTICA XCP (Articoli Gerhò Aggiornati) ---
    with tab_xcp:
        st.header("🛠️ Registro e Tracciabilità Centratori XCP Rinn")
        st.caption("Prontuario ufficiale per i dispositivi di centraggio radiografico endorale. Codici allineati con i numeri articolo del catalogo Gerhò.")
        
        ricerca_xcp = st.text_input("Filtra rapidamente per nome dispositivo o Codice Articolo:", key="search_xcp")
        
        for item in STRUMENTARIO_XCP:
            if ricerca_xcp.lower() in item["nome"].lower() or ricerca_xcp.lower() in item["ref"].lower():
                with st.container():
                    col_img, col_info = st.columns([1, 2])
                    
                    with col_img:
                        st.image(item["immagine"], caption=item["nome"], use_container_width=True)
                    
                    with col_info:
                        st.subheader(item["nome"])
                        c1, c2 = st.columns(2)
                        c1.metric(label="Codice Articolo Gerhò", value=item["ref"])
                        c2.metric(label="Categoria Prodotto", value=item["tipo"])
                        
                        st.markdown(f"📍 **Collocazione / Uso prevalente:** `{item['ambulatorio']}`")
                        st.markdown(f"📝 **Indicazioni e specifiche cliniche:** {item['descrizione']}")
                    
                    st.markdown("---")

    # --- TAB 3: MAPPA INTERATTIVA ---
    with tab_mappa:
        st.header("Mappa Interattiva dell'Ambulatorio")
        html_content = """
        <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
        .container { position: relative; width: 100%; max-width: 900px; margin: 0 auto; }
        .image { display: block; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .hotspot { position: absolute; width: 26px; height: 26px; background-color: #FF4B4B; border-radius: 50%; cursor: pointer; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.6); animation: pulse 2.5s infinite; z-index: 10; }
        #hp1 { top: 65%; left: 45%; } #hp2 { top: 25%; left: 50%; } #hp3 { top: 70%; left: 22%; } #hp4 { top: 60%; left: 63%; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.8); } 70% { box-shadow: 0 0 0 12px rgba(255, 75, 75, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); } }
        .modal { display: none; position: absolute; top: 20%; left: 75%; background-color: white; padding: 16px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); width: 250px; z-index: 100; border-left: 5px solid #FF4B4B; font-family: sans-serif; }
        .modal h4 { margin: 0 0 6px 0; color: #31333F; font-size: 15px; }
        .modal p { margin: 0; font-size: 12.5px; color: #555; line-height: 1.4; }
        .close-btn { float: right; cursor: pointer; font-weight: bold; color: #999; font-size: 16px; }
        </style></head><body><div class="container">
          <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=900&q=80" class="image">
          <div class="hotspot" id="hp1" onclick="showInfo('Riunito Odontoiatrico', 'Poltrona del paziente a movimentazione elettromeccanica. Checklist: Eseguire la decontaminazione dei circuiti idrici (sistema Flushing) all inizio di ogni turno.')"></div>
          <div class="hotspot" id="hp2" onclick="showInfo('Lampada Scialitica', 'Sorgente luminosa orientabile a LED per il campo operatorio. Checklist: Pulire esclusivamente a freddo con detergenti non alcolici sulle parabole.')"></div>
          <div class="hotspot" id="hp3" onclick="showInfo('Consolle Servomobile Strumenti', 'Supporto principale per manipoli. Checklist: Lubrificare i manipoli dopo ogni ciclo d uso prima dell imbustamento e passaggio in autoclave.')"></div>
          <div class="hotspot" id="hp4" onclick="showInfo('Area Stoccaggio e Lavello', 'Piano di lavoro per la preparazione dei materiali. Checklist: Mantenere la netta separazione tra area sporca e area pulita.')"></div>
          <div id="infoModal" class="modal"><span class="close-btn" onclick="closeModal()">&times;</span><h4 id="modalTitle">Componente</h4><p id="modalDesc"></p></div>
        </div><script>
        function showInfo(title, text) { document.getElementById("modalTitle").innerText = title; document.getElementById("modalDesc").innerText = text; document.getElementById("infoModal").style.display = "block"; }
        function closeModal() { document.getElementById("infoModal").style.display = "none"; }
        </script></body></html>
        """
        components.html(html_content, height=650, scrolling=False)

    # --- TAB 4: GAMIFICATION E AUTOVALUTAZIONE (RIPRISTINATO) ---
    with tab_esercitati:
        st.header("🎯 Sistema di Autovalutazione e Gamification")
        col_quiz, col_classifica = st.columns([6, 4])
        
        with col_quiz:
            st.subheader("🛠️ Configura la tua Esercitazione")
            if not st.session_state["quiz_attivo"]:
                btn_argomento, btn_tutto = st.columns(2)
                with btn_argomento:
                    if st.button("📚 Esercitati per Argomento", use_container_width=True):
                        argomento = random.choice(list(QUIZ_DATA.keys()))
                        st.session_state["domande_selezionate"] = QUIZ_DATA[argomento]
                        st.session_state["quiz_attivo"] = True
                        st.session_state["indice_domanda"] = 0
                        st.session_state["punteggio_sessione"] = 0
                        st.rerun()
                with btn_tutto:
                    if st.button("🌐 Esercitati su Tutto", use_container_width=True):
                        tutte_le_domande = []
                        for lista in QUIZ_DATA.values():
                            tutte_le_domande.extend(lista)
                        random.shuffle(tutte_le_domande)
                        st.session_state["domande_selezionate"] = tutte_le_domande
                        st.session_state["quiz_attivo"] = True
                        st.session_state["indice_domanda"] = 0
                        st.session_state["punteggio_sessione"] = 0
                        st.rerun()
                st.info("Scegli una modalità per avviare il set di domande interattive di reparto.")
            else:
                lista_domande = st.session_state["domande_selezionate"]
                attuale = st.session_state["indice_domanda"]
                
                if attuale < len(lista_domande):
                    dati_domanda = lista_domande[attuale]
                    st.markdown(f"**Domanda {attuale + 1} di {len(lista_domande)}**")
                    st.info(dati_domanda["domanda"])
                    risposta = st.radio("Seleziona la risposta corretta:", dati_domanda["opzioni"], key=f"q_{attuale}")
                    
                    if st.form_submit_button if False else st.button("Conferma Risposta ➔", use_container_width=True):
                        if risposta == dati_domanda["corretta"]:
                            st.session_state["punteggio_sessione"] += 10
                        st.session_state["indice_domanda"] += 1
                        st.rerun()
                else:
                    st.success(f"🎉 Esercitazione completata! Punteggio ottenuto: +{st.session_state['punteggio_sessione']} punti.")
                    nome_utente_attuale = USER_DB[st.session_state["username"]]["nome_completo"]
                    st.session_state["classifica"][nome_utente_attuale] += st.session_state["punteggio_sessione"]
                    
                    if st.button("Chiudi e Salva in Classifica", use_container_width=True):
                        st.session_state["quiz_attivo"] = False
                        st.rerun()

        with col_classifica:
            st.subheader("🏆 Classifica di Studio")
            classifica_ordinata = sorted(st.session_state["classifica"].items(), key=lambda item: item[1], reverse=True)
            for posizione, (operatore, punti) in enumerate(classifica_ordinata, start=1):
                medaglia = "🥇" if posizione == 1 else "🥈" if posizione == 2 else "🥉" if posizione == 3 else "👤"
                nome_connesso = USER_DB[st.session_state["username"]]["nome_completo"]
                if operatore == nome_connesso:
                    st.markdown(f"**{medaglia} Posizione {posizione}: {operatore} — {punti} PT (Tu)** 🌟")
                else:
                    st.markdown(f"{medaglia} Posizione {posizione}: {operatore} — {punti} PT")
