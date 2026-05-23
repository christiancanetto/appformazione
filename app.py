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

# 2. DATABASE DELLE PROCEDURE (Utilizzato dall'Assistente AI)
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
    
    "Procedure ambulatorio di Protesi - Assistenza alla poltrona": 
        "Preparazione del vassoio per impronte (siliconi per addizione/condensazione o scanner intraorale). "
        "Gestione dei cementi provvisori e definitivi. Manipolazione corretta dei materiali da ribasatura. "
        "Disinfezione di livello intermedio dei manufatti protesici prima dell'invio o della ricezione dal laboratorio odontotecnico.",
    
    "Procedure ambulatorio Ortodonzia - Assistenza alla poltrona": 
        "Allestimento del kit per bandaggio: archi ortodontici preformati, attacchi (bracket), pinze di utilità (Weingart, Ash) e tronchesi. "
        "Preparazione dell'acido ortofosforico per il mordenzamento e dell'adesivo fotopolimerizzabile. "
        "Istruzione del paziente sull'igiene orale domiciliare in presenza di dispositivi fissi o allineatori.",
    
    "Procedure ambulatorio Conservativa - Assistenza alla poltrona": 
        "Predisposizione dei sistemi di isolamento del campo (Diga di gomma: fogli, uncini, pinza foradiga e arco). "
        "Organizzazione sequenziale delle matrici sezionali e cunei. Assistenza durante la rimozione del tessuto carioso "
        "e passaggio ordinato di: mordenzante, adesivo, compositi fluidi e condensabili, lampada polimerizzatrice."
}

# 3. CATALOGO STRUMENTARIO E FERRI ORTODONTICI (Riferimento Catalogo Gerhò)
STRUMENTARIO_ORTO = [
    {
        "nome": "Pinza di Weingart",
        "ref": "GH-3402",
        "tipo": "Utility / Bandaggio",
        "ambulatorio": "Ambulatorio di Ortodonzia (Studio 2)",
        "descrizione": "Pinza universale con punte zigrinate e curve per afferrare e guidare l'arco ortodontico durante l'inserimento nei tubi e nei bracket. Massima presa senza danneggiare il filo.",
        "immagine": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=400&q=80"
    },
    {
        "nome": "Tronchese di Taglio Distale",
        "ref": "GH-3115",
        "tipo": "Taglio fili duri",
        "ambulatorio": "Ambulatorio di Ortodonzia (Studio 2)",
        "descrizione": "Tronchese con sistema di ritenuta del filo reciso. Taglia l'arco a filo della scanalatura del tubo vestibolare trattenendo lo spezzone per evitare che cada nella bocca del paziente.",
        "immagine": "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=400&q=80"
    },
    {
        "nome": "Pinza di Adams",
        "ref": "GH-3208",
        "tipo": "Piegatura fili / Lab",
        "ambulatorio": "Ambulatorio di Ortodonzia e Laboratorio interno",
        "descrizione": "Pinza classica per la formatura e la piegatura precisa di fili ortodontici rigidi e per l'adattamento dei ganci di tenuta degli apparecchi mobili (fili fino a 0.7mm).",
        "immagine": "https://images.unsplash.com/photo-1512223792601-592a9809eed4?auto=format&fit=crop&w=400&q=80"
    },
    {
        "nome": "Posizionatore di Bracket (Gauge)",
        "ref": "GH-1104",
        "tipo": "Posizionamento / Misura",
        "ambulatorio": "Ambulatorio di Ortodonzia (Studio 2)",
        "descrizione": "Strumento a croce millimetrato per determinare l'esatta altezza dello slot del bracket rispetto al margine incisale o occlusale dell'elemento dentario (misure 3.5 - 4.0 - 4.5 - 5.0 mm).",
        "immagine": "https://images.unsplash.com/photo-1579684389782-64d84b5e901a?auto=format&fit=crop&w=400&q=80"
    }
]

# 4. POOL DI DOMANDE PER IL SISTEMA DI GAMIFICATION
QUIZ_DATA = {
    "Accoglienza e Magazzino": [
        {"domanda": "Quale test si esegue per verificare la penetrazione del vapore nei corpi cavi in autoclave?", "opzioni": ["Bowie & Dick Test", "Helix Test", "Spore Test"], "corretta": "Helix Test"},
        {"domanda": "Cosa si verifica prioritariamente nella fase di presa in carico del paziente?", "opzioni": ["L'appuntamento successivo", "L'anamnesi recente e il consenso firmato", "Il pagamento del saldo"], "corretta": "L'anamnesi recente e il consenso firmato"}
    ],
    "Assistenza alla Poltrona": [
        {"domanda": "Quale materiale necessita di acido ortofosforico per il mordenzamento in Conservativa?", "opzioni": ["L'idrossido di calcio", "Lo smalto e la dentina per l'adesivo", "L'ossido di zinco eugenolo"], "corretta": "Lo smalto e la dentina per l'adesivo"},
        {"domanda": "Quali pinze sono considerate di utilità generale in Ortodonzia?", "opzioni": ["Pinze di Weingart e Ash", "Pinze di Pean", "Pinze da estrazione"], "corretta": "Pinze di Weingart e Ash"},
        {"domanda": "Come vanno trattati i manufatti protesici prima dell'invio al laboratorio?", "opzioni": ["Solo sciacquati con acqua", "Disinfettati con livello intermedio", "Sterilizzati in autoclave"], "corretta": "Disinfettati con livello intermedio"}
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

# 7. AREA APPLICAZIONE
else:
    with st.sidebar:
        st.subheader(f"👤 {st.session_state['username']}")
        st.info(f"Ruolo: **{st.session_state['ruolo']}**")
        if st.button("Effettua Logout", use_container_width=True):
            st.session_state["autenticato"] = False
            st.rerun()

    st.title("🦷 Hub Operativo e Linee Guida di Studio")
    
    # --- ASSISTENTE AI POTENZIATO CON SCANSIONE DEI CODICI REF E FERRI ---
    st.markdown("---")
    with st.container():
        st.markdown("### 🤖 Assistente AI - Supporto Decisionale Clinico")
        st.caption("L'Intelligenza Artificiale analizza in tempo reale i protocolli dello studio e l'inventario dei ferri Gerhò.")
        
        query_ai = st.text_input("Formula una domanda clinica, logistica o inserisci un codice REF (es. 'A cosa serve il codice GH-3115?'):", placeholder="Chiedi all'AI...")
        
        if query_ai:
            query_clean = query_ai.lower()
            risposta_trovata = False
            
            # 1. CONTROLLO AI SUL CATALOGO DEI FERRI CHIRURGICI
            for ferro in STRUMENTARIO_ORTO:
                if query_clean in ferro["nome"].lower() or query_clean in ferro["ref"].lower() or query_clean in ferro["tipo"].lower():
                    st.markdown(f"**🤖 Risposta dell'Assistente AI (Identificato Strumento da Inventario):**")
                    st.success(f"Ho trovato una corrispondenza nel catalogo **Gerhò**:\n\n"
                               f"🔹 **Strumento**: {ferro['nome']} (Codice REF: `{ferro['ref']}`)\n"
                               f"📍 **Uso Prevalente**: {ferro['ambulatorio']}\n"
                               f"📝 **Dettagli d'uso**: {ferro['descrizione']}")
                    risposta_trovata = True
                    break
            
            # 2. CONTROLLO SEZIONE PROCEDURE (se non ha trovato corrispondenza tra i ferri)
            if not risposta_trovata:
                for titolo_proc, contenuto_proc in PROCEDURE_DETTAGLI.items():
                    parole_chiave = [w for w in query_clean.split() if len(w) > 4]
                    if any(parola in titolo_proc.lower() or parola in contenuto_proc.lower() for parola in parole_chiave):
                        st.markdown(f"**🤖 Risposta dell'Assistente AI (Estratta da: *{titolo_proc}*):**")
                        st.info(f"In base al protocollo ufficiale dello studio relativo a **{titolo_proc}**, ecco le indicazioni operative: \n\n"
                                f"*{contenuto_proc}*\n\n"
                                f"⚠️ **Nota dell'IA:** Assicurarsi che ogni azione sia tracciata nel registro informatizzato.")
                        risposta_trovata = True
                        break
            
            if not risposta_trovata:
                st.warning("🤖 **Risposta dell'Assistente AI:** La richiesta non trova un riscontro nei protocolli o nello strumentario attuale.")
                
    st.markdown("---")

    # Navigazione principale dei Tab (Inclusa la nuova scheda Ferri)
    tab_procedure, tab_ferri, tab_mappa, tab_esercitati = st.tabs([
        "📋 Procedure Cliniche", 
        "🛠️ Strumentario Ortodonzia (Gerhò)", 
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
                        st.button(f"︎🤝 {up_c}", key=f"up_{proc}", on_click=vota_up, args=(proc,), help="Procedura Chiara", use_container_width=True)
                    with sub_col2:
                        st.button(f"︎⚠ {down_c}", key=f"down_{proc}", on_click=vota_down, args=(proc,), help="Richiede Revisione", use_container_width=True)
                
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

    # --- NUOVO TAB 2: STRUMENTARIO ORTODONZIA (Riferimento Gerhò) ---
    with tab_ferri:
        st.header("🛠️ Registro e Tracciabilità Ferri da Ortodonzia")
        st.caption("Prontuario dei dispositivi medici e delle pinze specialistiche utilizzate nell'Unità Operativa. Codici REF validati su catalogo Gerhò.")
        
        # Filtro rapido di ricerca interno alla scheda
        ricerca_ferro = st.text_input("Filtra rapidamente per nome strumento o codice REF:", key="search_ferri")
        
        for item in STRUMENTARIO_ORTO:
            if ricerca_ferro.lower() in item["nome"].lower() or ricerca_ferro.lower() in item["ref"].lower():
                with st.container():
                    # Layout pulito a due colonne per ottimizzare lo scorrimento verticale ed esaltare l'immagine del ferro
                    col_img, col_info = st.columns([1, 2])
                    
                    with col_img:
                        st.image(item["immagine"], caption=item["nome"], use_container_width=True)
                    
                    with col_info:
                        st.subheader(item["nome"])
                        
                        # Utilizzo di metriche visive per evidenziare i dati chiave per l'assistente
                        c1, c2 = st.columns(2)
                        c1.metric(label="Codice REF articolo (Gerhò)", value=item["ref"])
                        c2.metric(label="Uso Principale", value=item["tipo"])
                        
                        st.markdown(f"📍 **Ambulatorio di pertinenza principale:** `{item['ambulatorio']}`")
                        st.markdown(f"📝 **Indicazioni cliniche e manutenzione:** {item['descrizione']}")
                    
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

    # --- TAB 4: GAMIFICATION ---
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
                st.info("Scegli una modalità per avviare il set di domande interattive.")
            else:
                lista_domande = st.session_state["domande_selezionate"]
                attuale = st.session_state["indice_domanda"]
                if attuale < len(lista_domande):
                    dati_domanda = lista_domande[attuale]
                    st.markdown(f"**Domanda {attuale + 1} di {len(lista_domande)}**")
                    st.info(dati_domanda["domanda"])
                    risposta = st.radio("Seleziona la risposta corretta:", dati_domanda["opzioni"], key=f"q_{attuale}")
                    if st.button("Conferma Risposta ➔", use_container_width=True):
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
