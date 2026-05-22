import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina
st.set_page_config(
    page_title="Gestione Procedure & Hub Interattivo",
    page_icon="📋",
    layout="wide"
)

# 1. DATABASE UTENTI SIMULATO (Dizionario Python)
USER_DB = {
    "admin_founder": {"password": "password123", "ruolo": "Founder"},
    "mod_user": {"password": "password456", "ruolo": "Moderatore"},
    "base_user": {"password": "password789", "ruolo": "Base"}
}

# 2. INIZIALIZZAZIONE DELLO STATO DELLA SESSIONE
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False
    st.session_state["username"] = ""
    st.session_state["ruolo"] = ""

if "commenti" not in st.session_state:
    st.session_state["commenti"] = {
        "Procedura 1": ["Ottima guida, molto chiara.", "Manca un passaggio sul controllo finale."],
        "Procedura 2": ["Applicata oggi in reparto, funziona perfettamente."],
        "Procedura 3": []
    }

# Funzione di supporto per eliminare in sicurezza un commento evitando i bug di ciclo
def elimina_commento(procedura, indice):
    st.session_state["commenti"][procedura].pop(indice)
    st.toast("✅ Commento rimosso con successo!")

# 3. INTERFACCIA DI LOGIN
if not st.session_state["autenticato"]:
    st.title("🔒 Accesso al Sistema")
    st.caption("Inserisci le tue credenziali per accedere alle procedure e alla mappa interattiva.")
    
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
                    st.success(f"Benvenuto {username_input}!")
                    st.rerun()
                else:
                    st.error("Credenziali errate. Riprova.")
                    
        with st.expander("ℹ️ Credenziali di test disponibili"):
            st.markdown("""
            * **Founder**: `admin_founder` / `password123`
            * **Moderatore**: `mod_user` / `password456`
            * **Base**: `base_user` / `password789`
            """)

# 4. AREA APPLICAZIONE (Se autenticati)
else:
    with st.sidebar:
        st.subheader(f"👤 {st.session_state['username']}")
        st.info(f"Ruolo: **{st.session_state['ruolo']}**")
        if st.button("Effettua Logout", use_container_width=True):
            st.session_state["autenticato"] = False
            st.session_state["username"] = ""
            st.session_state["ruolo"] = ""
            st.rerun()

    st.title("🚀 Hub di Gestione Interna")
    
    tab_procedure, tab_mappa = st.tabs(["📋 Procedure Operative", "🗺️ Mappa Interattiva (HTML/CSS)"])

    # --- TAB 1: PROCEDURE E COMMENTI (Versione Corretta e Stabile) ---
    with tab_procedure:
        st.header("Elenco Procedure e Feedback")
        
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
                
                st.markdown("**Commenti degli utenti:**")
                lista_commenti = st.session_state["commenti"][proc]
                
                if lista_commenti:
                    # Usiamo un approccio pulito senza colonne conflittuali per i bottoni distruttivi
                    for idx, commento in enumerate(lista_commenti):
                        st.markdown(f" {commento}")
                        
                        # Mostra il bottone elimina solo a Founder e Moderatore
                        if st.session_state["ruolo"] in ["Founder", "Moderatore"]:
                            # Usiamo on_click per eseguire l'azione prima del rinfresco della pagina
                            st.button(
                                f"🗑️ Elimina questo commento", 
                                key=f"del_{proc}_{idx}", 
                                size="small",
                                on_click=elimina_commento, 
                                args=(proc, idx)
                            )
                        st.write("")
                else:
                    st.info("Non ci sono ancora commenti per questa procedura.")
                
                # Form di inserimento commento
                with st.form(key=f"form_{proc}", clear_on_submit=True):
                    nuovo_commento = st.text_area("Aggiungi un commento operativo:", max_chars=200, key=f"txt_{proc}")
                    submit_commento = st.form_submit_button("Invia Commento")
                    
                    if submit_commento and nuovo_commento.strip() != "":
                        testo_finale = f"[{st.session_state['ruolo']}] {st.session_state['username']}: {nuovo_commento}"
                        st.session_state["commenti"][proc].append(testo_finale)
                        st.rerun()

    # --- TAB 2: IMMAGINE E PUNTO INTERATTIVO ---
    with tab_mappa:
        st.header("Visualizzazione con Hotspot Interattivo")
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        .container { position: relative; width: 100%; max-width: 800px; margin: 0 auto; }
        .image { display: block; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
        .hotspot {
          position: absolute;
          top: 40%; left: 60%; transform: translate(-50%, -50%);
          width: 24px; height: 24px; background-color: #FF4B4B; border-radius: 50%; cursor: pointer;
          border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5);
          animation: pulse 2s infinite; transition: transform 0.2s ease;
        }
        .hotspot:hover { transform: translate(-50%, -50%) scale(1.3); }
        @keyframes pulse {
          0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
          70% { box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
          100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
        }
        .modal {
          display: none; position: absolute; top: 45%; left: 60%; transform: translateX(-50%);
          background-color: white; padding: 15px; border-radius: 6px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.25); width: 220px; z-index: 100; border-top: 4px solid #FF4B4B;
          font-family: sans-serif;
        }
        .modal h4 { margin: 0 0 8px 0; color: #31333F; }
        .modal p { margin: 0; font-size: 13px; color: #555; line-height: 1.4; }
        .close-btn { float: right; cursor: pointer; font-weight: bold; color: #aaa; }
        .close-btn:hover { color: #000; }
        </style>
        </head>
        <body>
        <div class="container">
          <img src="https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80" alt="Workplace" class="image">
          <div class="hotspot" onclick="toggleModal()"></div>
          <div id="infoModal" class="modal">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h4>Core Server Alpha</h4>
            <p>Questo nodo gestisce la sincronizzazione in tempo reale delle procedure. Stato: <b>Attivo</b>.</p>
          </div>
        </div>
        <script>
        function toggleModal() {
          var modal = document.getElementById("infoModal");
          modal.style.display = (modal.style.display === "block") ? "none" : "block";
        }
        function closeModal() { document.getElementById("infoModal").style.display = "none"; }
        </script>
        </body>
        </html>
        """
        components.html(html_content, height=500, scrolling=False)
