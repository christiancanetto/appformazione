import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina (deve essere la prima istruzione Streamlit)
st.set_page_config(
    page_title="Gestione Procedure & Hub Interattivo",
    page_icon="📋",
    layout="wide"
)

# 1. DATABASE UTENTI SIMULATO (Dizionario Python)
# Formato: "username": {"password": "...", "ruolo": "..."}
USER_DB = {
    # Amministratore supremo con permessi di cancellazione
    "admin_founder": {"password": "password123", "ruolo": "Founder"},
    # Gestore dei contenuti con permessi di cancellazione
    "mod_user": {"password": "password456", "ruolo": "Moderatore"},
    # Utente standard (può solo leggere e commentare)
    "base_user": {"password": "password789", "ruolo": "Base"}
}

# 2. INIZIALIZZAZIONE DELLO STATO DELLA SESSIONE (st.session_state)
# Mantiene i dati attivi durante i ricarichi della pagina
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False
    st.session_state["username"] = ""
    st.session_state["ruolo"] = ""

if "commenti" not in st.session_state:
    # Struttura dati iniziale per i commenti delle tre procedure
    st.session_state["commenti"] = {
        "Procedura 1": ["Ottima guida, molto chiara.", "Manca un passaggio sul controllo finale."],
        "Procedura 2": ["Applicata oggi in reparto, funziona perfettamente."],
        "Procedura 3": []
    }

# 3. INTERFACCIA DI LOGIN
if not st.session_state["autenticato"]:
    st.title("🔒 Accesso al Sistema")
    st.caption("Inserisci le tue credenziali per accedere alle procedure e alla mappa interattiva.")
    
    # Form di login pulito ed centrato visivamente
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
                    st.success(f"Benvenuto {username_input}! Ruolo: {st.session_state['ruolo']}")
                    st.rerun()
                else:
                    st.error("Credenziali errate. Riprova.")
                    
        # Info box per i test rapidi su Streamlit Cloud
        with st.expander("ℹ️ Credenziali di test disponibili"):
            st.markdown("""
            * **Founder**: `admin_founder` / `password123`
            * **Moderatore**: `mod_user` / `password456`
            * **Base**: `base_user` / `password789`
            """)

# 4. AREA APPLICAZIONE (Accessibile solo se autenticati)
else:
    # Barra laterale con informazioni utente e logout
    with st.sidebar:
        st.subheader(f"👤 Utente: {st.session_state['username']}")
        st.info(f"Ruolo: **{st.session_state['ruolo']}**")
        if st.button("Effettua Logout", use_container_width=True):
            st.session_state["autenticato"] = False
            st.session_state["username"] = ""
            st.session_state["ruolo"] = ""
            st.rerun()

    st.title("🚀 Hub di Gestione Interna")
    st.write("Benvenuto nel pannello operativo. Naviga tra le schede per gestire i dati.")

    # Creazione dei Tab dell'applicazione
    tab_procedure, tab_mappa = st.tabs(["📋 Procedure Operative", "🗺️ Mappa Interattiva (HTML/CSS)"])

    # --- TAB 1: PROCEDURE E COMMENTI ---
    with tab_procedure:
        st.header("Elenco Procedure e Feedback")
        
        # Lista di 3 procedure d'esempio
        procedure_list = ["Procedura 1", "Procedura 2", "Procedura 3"]
        descrizioni = {
            "Procedura 1": "Protocollo standard per l'accettazione e la digitalizzazione dei dati nel sistema centrale.",
            "Procedura 2": "Linee guida per la manutenzione ordinaria delle apparecchiature e verifica dei log di sistema.",
            "Procedura 3": "Procedura di emergenza per il ripristino del database in caso di disconnessione della rete."
        }
        
        for proc in procedure_list:
            with st.expander(f"🔍 {proc} - Dettagli e Discussione", expanded=True):
                st.markdown(f"**Descrizione:** {descrizioni[proc]}")
                st.write("---")
                
                # Visualizzazione dei commenti esistenti
                st.markdown("**Commenti degli utenti:**")
                if st.session_state["commenti"][proc]:
                    for idx, commento in enumerate(st.session_state["commenti"][proc]):
                        col_text, col_action = st.columns([5, 1])
                        with col_text:
                            st.caption(f"💬 {commento}")
                        
                        # Controllo dei permessi: solo Founder o Moderatore vedono il tasto cancella
                        with col_action:
                            if st.session_state["ruolo"] in ["Founder", "Moderatore"]:
                                if st.button("Elimina", key=f"del_{proc}_{idx}", size="small", type="secondary"):
                                    st.session_state["commenti"][proc].pop(idx)
                                    st.success("Commento rimosso!")
                                    st.rerun()
                else:
                    st.info("Non ci sono ancora commenti per questa procedura.")
                
                # Form per inserire un nuovo commento (Accessibile a tutti i ruoli)
                with st.form(key=f"form_{proc}", clear_on_submit=True):
                    nuovo_commento = st.text_area("Aggiungi un commento operativo:", max_chars=200, placeholder="Scrivi qui...")
                    submit_commento = st.form_submit_button("Invia Commento")
                    
                    if submit_commento and nuovo_commento.strip() != "":
                        # Aggiunge il nome utente e il ruolo per tracciabilità
                        testo_finale = f"[{st.session_state['ruolo']}] {st.session_state['username']}: {nuovo_commento}"
                        st.session_state["commenti"][proc].append(testo_finale)
                        st.success("Commento aggiunto con successo!")
                        st.rerun()

    # --- TAB 2: IMMAGINE E PUNTO INTERATTIVO (HTML/CSS) ---
    with tab_mappa:
        st.header("Visualizzazione con Hotspot Interattivo")
        st.write("Passa il mouse o clicca sul punto evidenziato sopra l'immagine per scoprire le informazioni dettagliate.")

        # Codice HTML, CSS e JavaScript integrato per creare l'effetto overlay
        # Utilizza un'immagine segnaposto ad alta risoluzione orientata al tech/workplace
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        /* Contenitore principale responsivo */
        .container {
          position: relative;
          width: 100%;
          max-width: 800px;
          margin: 0 auto;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* L'immagine di sfondo dell'interfaccia */
        .image {
          display: block;
          width: 100%;
          height: auto;
          border-radius: 8px;
          box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }

        /* Stile del punto interattivo (Hotspot) */
        .hotspot {
          position: absolute;
          /* Posizionamento percentuale calcolato sull'immagine */
          top: 40%; 
          left: 60%;
          transform: translate(-50%, -50%);
          
          /* Estetica del punto */
          width: 24px;
          height: 24px;
          background-color: #FF4B4B; /* Colore rosso coordinato a Streamlit */
          border-radius: 50%;
          cursor: pointer;
          border: 3px solid white;
          box-shadow: 0 0 10px rgba(0,0,0,0.5);
          
          /* Animazione a impulso per attirare l'attenzione */
          animation: pulse 2s infinite;
          transition: transform 0.2s ease;
        }
        
        .hotspot:hover {
          transform: translate(-50%, -50%) scale(1.3);
        }

        @keyframes pulse {
          0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
          70% { box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
          100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
        }

        /* Stile del Pop-up (Modal nascosto di default) */
        .modal {
          display: none; 
          position: absolute;
          top: 45%;
          left: 60%;
          transform: translateX(-50%);
          background-color: white;
          padding: 15px;
          border-radius: 6px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.25);
          width: 220px;
          z-index: 100;
          border-top: 4px solid #FF4B4B;
        }

        .modal h4 {
          margin: 0 0 8px 0;
          color: #31333F;
        }

        .modal p {
          margin: 0;
          font-size: 13px;
          color: #555;
          line-height: 1.4;
        }

        .close-btn {
          float: right;
          cursor: pointer;
          font-weight: bold;
          color: #aaa;
        }
        .close-btn:hover { color: #000; }
        </style>
        </head>
        <body>

        <div class="container">
          <!-- Immagine mockup strutturale di un ufficio/tecnologia -->
          <img src="https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80" alt="Workplace" class="image">
          
          <!-- Punto interattivo sul monitor/dispositivo principale -->
          <div class="hotspot" onclick="toggleModal()"></div>

          <!-- Finestra Pop-up collegata -->
          <div id="infoModal" class="modal">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h4>Core Server Alpha</h4>
            <p>Questo nodo gestisce la sincronizzazione in tempo reale delle procedure di reparto. Stato: <b>Attivo</b>.</p>
          </div>
        </div>

        <script>
        // Logica JavaScript per aprire e chiudere il box informativo
        function toggleModal() {
          var modal = document.getElementById("infoModal");
          if (modal.style.display === "block") {
            modal.style.display = "none";
          } else {
            modal.style.display = "block";
          }
        }
        
        function closeModal() {
          document.getElementById("infoModal").style.display = "none";
        }
        </script>

        </body>
        </html>
        """
        
        # Integrazione sicura del codice HTML all'interno del layout Streamlit
        components.html(html_content, height=500, scrolling=False)