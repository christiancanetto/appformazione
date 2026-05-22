import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina
st.set_page_config(
    page_title="Pannello Operativo Ambulatorio Odontoiatrico",
    page_icon="🦷",
    layout="wide"
)

# 1. DATABASE UTENTI SIMULATO
USER_DB = {
    "admin_founder": {"password": "password123", "ruolo": "Founder"},
    "mod_user": {"password": "password456", "ruolo": "Moderatore"},
    "base_user": {"password": "password789", "ruolo": "Base"}
}

# 2. DIZIONARIO DELLE PROCEDURE STRUTTURATE
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

# 3. INIZIALIZZAZIONE DELLO STATO DELLA SESSIONE (st.session_state)
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False
    st.session_state["username"] = ""
    st.session_state["ruolo"] = ""

# Inizializzazione sicura dei commenti per le nuove procedure
if "commenti" not in st.session_state:
    st.session_state["commenti"] = {titolo: [] for titolo in PROCEDURE_DETTAGLI.keys()}
    # Aggiungiamo un commento di test iniziale sulla prima procedura
    st.session_state["commenti"]["Presa in carico del paziente presso gli studi odontoiatrici"].append(
        "[Base] base_user: Ricordarsi di far compilare il modulo privacy aggiornato ai nuovi pazienti."
    )

# Inizializzazione dei feedback Up/Down (Voti)
if "voti" not in st.session_state:
    st.session_state["voti"] = {titolo: {"up": 0, "down": 0} for titolo in PROCEDURE_DETTAGLI.keys()}

# Funzione per eliminare i commenti
def elimina_commento(procedura, indice):
    st.session_state["commenti"][procedura].pop(indice)
    st.toast("✅ Commento rimosso con successo!")

# Funzioni per gestire i voti
def vota_up(procedura):
    st.session_state["voti"][procedura]["up"] += 1
    st.toast("👍 Feedback positivo registrato")

def vota_down(procedura):
    st.session_state["voti"][procedura]["down"] += 1
    st.toast("👎 Feedback negativo registrato")


# 4. INTERFACCIA DI LOGIN
if not st.session_state["autenticato"]:
    st.title("🔒 Piattaforma Sperimentale Odontoiatrica")
    st.caption("Accesso riservato al personale dello studio per la revisione delle procedure interne.")
    
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
                    st.error("Credenziali errate. Riprova.")
                    
        with st.expander("ℹ️ Utenze operative di test"):
            st.markdown("""
            * **Founder**: `admin_founder` / `password123`
            * **Moderatore**: `mod_user` / `password456`
            * **Base**: `base_user` / `password789`
            """)

# 5. AREA APPLICAZIONE (Se autenticati)
else:
    with st.sidebar:
        st.subheader(f"👤 {st.session_state['username']}")
        st.info(f"Ruolo: **{st.session_state['ruolo']}**")
        if st.button("Effettua Logout", use_container_width=True):
            st.session_state["autenticato"] = False
            st.session_state["username"] = ""
            st.session_state["ruolo"] = ""
            st.rerun()

    st.title("🦷 Hub Operativo e Linee Guida di Studio")
    
    tab_procedure, tab_mappa = st.tabs(["📋 Procedure Cliniche", "🗺️ Anatomia dell'Ambulatorio"])

    # --- TAB 1: PROCEDURE CLINICHE, REAZIONI E COMMENTI ---
    with tab_procedure:
        st.header("Protocolli e Standard di Assistenza")
        st.write("Consulta le procedure, esprimi il tuo feedback sull'efficacia del protocollo e lascia note operative.")
        
        for proc, descrizione in PROCEDURE_DETTAGLI.items():
            with st.expander(f"📖 {proc}", expanded=False):
                st.markdown(f"**Protocollo Operativo:**")
                st.write(descrizione)
                
                # SEZIONE REAZIONI (Up / Down)
                st.write("")
                col_voti_info, col_btn_up, col_btn_down, _ = st.columns([2, 1, 1, 6])
                with col_voti_info:
                    up_count = st.session_state["voti"][proc]["up"]
                    down_count = st.session_state["voti"][proc]["down"]
                    st.markdown(f"**Valutazione Protocollo:** 👍 {up_count} | 👎 {down_count}")
                with col_btn_up:
                    st.button("👍 Utile", key=f"up_{proc}", on_click=vota_up, args=(proc,))
                with col_btn_down:
                    st.button("👎 Da rivedere", key=f"down_{proc}", on_click=vota_down, args=(proc,))
                
                st.write("---")
                
                # SEZIONE COMMENTI
                st.markdown("**Discussione e Note di Reparto:**")
                lista_commenti = st.session_state["commenti"][proc]
                
                if lista_commenti:
                    for idx, commento in enumerate(lista_commenti):
                        st.markdown(f"{commento}")
                        if st.session_state["ruolo"] in ["Founder", "Moderatore"]:
                            st.button(
                                "🗑️ Elimina Nota", 
                                key=f"del_{proc}_{idx}", 
                                on_click=elimina_commento, 
                                args=(proc, idx)
                            )
                        st.write("")
                else:
                    st.info("Nessuna nota operativa inserita per questo protocollo.")
                
                # Form inserimento nota
                with st.form(key=f"form_{proc}", clear_on_submit=True):
                    nuovo_commento = st.text_area("Inserisci un'osservazione o segnalazione:", max_chars=200, key=f"txt_{proc}", placeholder="Es. Mancano i cunei di legno nella sesta sedia...")
                    submit_commento = st.form_submit_button("Invia Nota")
                    
                    if submit_commento and nuovo_commento.strip() != "":
                        testo_finale = f"[{st.session_state['ruolo']}] {st.session_state['username']}: {nuovo_commento}"
                        st.session_state["commenti"][proc].append(testo_finale)
                        st.rerun()

    # --- TAB 2: MAPPA INTERATTIVA DELL'AMBULATORIO ---
    with tab_mappa:
        st.header("Mappa Interattiva delle Componenti dell'Ambulatorio")
        st.write("Seleziona uno dei punti sensibili (hotspot rossi) per visualizzare la checklist di manutenzione e utilizzo della componente dell'unità odontoiatrica.")
        
        # HTML/CSS/JS con immagine clinica e 4 punti interattivi mappati percentualmente
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        .container { position: relative; width: 100%; max-width: 900px; margin: 0 auto; }
        .image { display: block; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        
        /* Stile base comune per gli Hotspot */
        .hotspot {
          position: absolute;
          width: 26px; height: 26px; background-color: #FF4B4B; border-radius: 50%; cursor: pointer;
          border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.6);
          animation: pulse 2.5s infinite; transition: transform 0.2s ease;
          z-index: 10;
        }
        .hotspot:hover { transform: scale(1.3); background-color: #31333F; }
        
        /* Coordinate percentuali calibrate sull'immagine clinica dell'ambulatorio */
        #hp1 { top: 65%; left: 45%; } /* Riunito / Poltrona */
        #hp2 { top: 25%; left: 50%; } /* Lampada Scialitica */
        #hp3 { top: 70%; left: 22%; } /* Consolle Servomobile Strumenti */
        #hp4 { top: 60%; left: 63%; } /* Area Mobile Stoccaggio / Lavello / Sterilizzazione */

        @keyframes pulse {
          0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.8); }
          70% { box-shadow: 0 0 0 12px rgba(255, 75, 75, 0); }
          100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
        }
        
        /* Pannello Informativo Popup fluttuante */
        .modal {
          display: none; position: absolute; top: 20%; left: 75%; 
          background-color: white; padding: 16px; border-radius: 8px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.3); width: 250px; z-index: 100; 
          border-left: 5px solid #FF4B4B; font-family: sans-serif;
        }
        .modal h4 { margin: 0 0 6px 0; color: #31333F; font-size: 15px; }
        .modal p { margin: 0; font-size: 12.5px; color: #555; line-height: 1.4; }
        .close-btn { float: right; cursor: pointer; font-weight: bold; color: #999; font-size: 16px; }
        .close-btn:hover { color: #000; }
        </style>
        </head>
        <body>

        <div class="container">
          <!-- Immagine di un ambulatorio odontoiatrico pulito ed ergonomico -->
          <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=900&q=80" alt="Ambulatorio Odontoiatrico" class="image">
          
          <!-- I 4 Hotspot Interattivi -->
          <div class="hotspot" id="hp1" onclick="showInfo('Riunito Odontoiatrico', 'Poltrona del paziente a movimentazione elettromeccanica. Checklist: Eseguire la decontaminazione dei circuiti idrici (sistema Flushing) all inizio di ogni turno e posizionare le pellicole protettive monouso su poggiatesta e braccioli.')"></div>
          <div class="hotspot" id="hp2" onclick="showInfo('Lampada Scialitica', 'Sorgente luminosa orientabile a LED per il campo operatorio. Checklist: Pulire esclusivamente a freddo con detergenti non alcolici sulle parabole per evitare l opacizzazione. Verificare l integrità delle maniglie sterilizzabili rimovibili.')"></div>
          <div class="hotspot" id="hp3" onclick="showInfo('Consolle Servomobile Strumenti', 'Supporto principale per manipoli (turbina, micromotore, ablatori, siringa aria-acqua). Checklist: Lubrificare i manipoli dopo ogni ciclo d uso prima dell imbustamento e passaggio in autoclave. Verificare la pressione del manometro.')"></div>
          <div class="hotspot" id="hp4" onclick="showInfo('Area Stoccaggio e Lavello di Unità', 'Piano di lavoro per la preparazione dei materiali e decontaminazione immediata dello strumentario. Checklist: Mantenere la netta separazione tra area sporca (smaltimento/lavaggio) e area pulita (allestimento vassoio clinico).')"></div>

          <!-- Finestra Informativa Unica -->
          <div id="infoModal" class="modal">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h4 id="modalTitle">Componente</h4>
            <p id="modalDesc">Passa il mouse o clicca su un punto.</p>
          </div>
        </div>

        <script>
        function showInfo(title, text) {
          document.getElementById("modalTitle").innerText = title;
          document.getElementById("modalDesc").innerText = text;
          document.getElementById("infoModal").style.display = "block";
        }
        function closeModal() { 
          document.getElementById("infoModal").style.display = "none"; 
        }
        </script>

        </body>
        </html>
        """
        components.html(html_content, height=650, scrolling=False)
