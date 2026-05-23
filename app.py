import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# CONFIGURAZIONE PAGINA
# ==========================================
st.set_page_config(
    page_title="Piattaforma Formazione - databUSL",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sezione di inizializzazione dello stato dell'applicazione
if "registro_presenze" not in st.session_state:
    st.session_state.registro_presenze = pd.DataFrame(columns=[
        "Data/Ora", "Operatore", "Corso / ID Evento", "Ruolo", "Esito Test", "Note"
    ])

if "checklist_requisiti" not in st.session_state:
    st.session_state.checklist_requisiti = {
        "Verifica Iscrizioni e Quote": False,
        "Controllo Funzionamento Proiettore / Audio": False,
        "Firma Registro Presenze Iniziale": False,
        "Distribuzione Materiale Didattico e Dispense": False,
        "Verifica Connessione Rete Sanitaria per i Test": False
    }

# Database Statico dei Corsi e dei Contenuti
STRUMENTARIO_XCP = [
    {
        "ref": "100121",
        "nome": "Corso BLSD - Rianimazione Cardiopolmonare Adulto/Pediatrico",
        "tipo": "Formazione Obbligatoria / Emergenza",
        "descrizione": "Addestramento teorico-pratico sulle manovre di rianimazione cardiopolmonare con utilizzo di defibrillatore semiautomatico esterno (DAE). Conforme alle ultime linee guida ILCOR/ERC. Validità biennale con certificazione regionale.",
        "immagine": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Aula Magna - Padiglione Formazione"
    },
    {
        "ref": "100122",
        "nome": "Gestione del Rischio Clinico e Prevenzione Errori Terapeutici",
        "tipo": "Sicurezza / Risk Management",
        "descrizione": "Analisi dei processi assistenziali e metodologie di identificazione, valutazione e gestione dei rischi in ambiente ospedaliero. Focus sulle raccomandazioni ministeriali per la prevenzione degli errori di terapia e la corretta identificazione del paziente.",
        "immagine": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Aula Formazione A - Piano Terra"
    },
    {
        "ref": "100123",
        "nome": "Prevenzione delle Infezioni Correlate all'Assistenza (ICA)",
        "tipo": "Igiene / Controllo Infezioni",
        "descrizione": "Corso focalizzato sulle buone pratiche di igiene delle mani, l'uso corretto dei dispositivi di protezione individuale (DPI) e i protocolli di sanificazione ambientale. Gestione dell'isolamento funzionale e sorveglianza dei patogeni multi-resistenti.",
        "immagine": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Aula Formazione B - Primo Piano"
    },
    {
        "ref": "100124",
        "nome": "La Cartella Clinica Elettronica e la Protezione dei Dati (GDPR)",
        "tipo": "Informatica / Aspetti Legali",
        "descrizione": "Guida operativa all'utilizzo dei sistemi informativi aziendali per la documentazione sanitaria. Approfondimento sugli obblighi normativi legati al segreto professionale, alla privacy del paziente e alla corretta gestione dei profili di accesso.",
        "immagine": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Laboratorio Informatico - Seminterrato"
    }
]

PROCEDURE_CARD = {
    "titolo": "Procedura Operativa Standard per l'Accreditamento ECM dei Corsi Residenziali",
    "codice": "POS-FORM-ECM-005-REV02",
    "ambulatori": ["Ufficio Formazione", "Aule Didattiche Presidio Ospedaliero"],
    "responsabile": "Dirigente Responsabile UOSD Formazione / Provider ECM",
    "obiettivi": [
        "Garantire il rispetto dei criteri Agenas per l'erogazione dei crediti formativi.",
        "Assicurare la corretta rilevazione delle presenze e la tracciabilità delle schede di valutazione.",
        "Standardizzare il flusso documentale dalla pianificazione dell'evento alla rendicontazione finale."
    ],
    "fasi": [
        {"fase": "1. Predisposizione Evento", "dettaglio": "Caricamento dell'evento sulla piattaforma Agenas almeno 30 giorni prima dell'inizio. Verifica dei CV dei docenti, del programma didattico e del conflitto di interessi. Generazione dei codici identificativi dell'evento."},
        {"fase": "2. Controllo Accessi", "dettaglio": "Rilevazione della presenza dei partecipanti tramite firma manuale su registro ufficiale o lettura ottica del badge aziendale all'ingresso e all'uscita di ogni singola sessione formativa."},
        {"fase": "3. Valutazione e Apprendimento", "dettaglio": "Somministrazione del test di verifica dell'apprendimento (domande a risposta multipla con doppia rotazione) e del questionario di gradimento della qualità percepita al termine delle ore di lezione."},
        {"fase": "4. Rendicontazione", "dettaglio": "Verifica del superamento del test (almeno 75% di risposte esatte) e della frequenza (almeno 90% delle ore totali). Invio del report finale all'ente nazionale entro 90 giorni dalla chiusura dell'evento."}
    ],
    "alert_sicurezza": "⚠️ NOTA DI CONFORMITÀ: La mancata corrispondenza tra le firme di presenza e i tracciati informatici dei test, o il mancato raggiungimento della soglia minima di frequenza, comporta l'annullamento immediato dell'attribuzione dei crediti formativi per il singolo discente, con obbligo di segnalazione nel report di sistema."
}

# ==========================================
# INTERFACCIA UTENTE PRINCIPALE
# ==========================================
st.title("🎓 databUSL - Portale Gestione Formazione Permanente")
st.subheader("Sistema di Tracciabilità dei Corsi, Registrazione Presenze e Verifiche ECM")
st.markdown("---")

tab_check, tab_xcp, tab_lavaggio, tab_procedura = st.tabs([
    "📋 CHECKLIST PRE-CORSO", 
    "📚 CATALOGO FORMATIVO", 
    "✍️ REGISTRO PRESENZE", 
    "📖 REGOLAMENTO ECM"
])

# --- TAB 1: CHECKLIST PRE-CORSO ---
with tab_check:
    st.header("📋 Verifiche Obbligatorie Prima dell'Inizio del Corso")
    st.caption("Controlli preliminari a cura del tutor d'aula per garantire la conformità agli standard organizzativi aziendali ed ECM.")
    
    col_check, col_status = st.columns([2, 1])
    
    with col_check:
        completati = 0
        for task in st.session_state.checklist_requisiti.keys():
            st.session_state.checklist_requisiti[task] = st.checkbox(task, value=st.session_state.checklist_requisiti[task])
            if st.session_state.checklist_requisiti[task]:
                completati += 1
                
    with col_status:
        totale_task = len(st.session_state.checklist_requisiti)
        percentuale = int((completati / totale_task) * 100)
        
        st.metric(label="Requisiti Verificati", value=f"{completati} / {totale_task}", delta=f"{percentuale}%")
        st.progress(completati / totale_task)
        
        if completati == totale_task:
            st.success("✅ Aula conforme! È possibile avviare la sessione formativa e consentire l'accesso ai discenti.")
        else:
            st.warning("⚠️ Controlli incompleti. Completare le verifiche logistiche e amministrative prima dell'arrivo del docente.")

# --- TAB 2: CATALOGO FORMATIVO ---
with tab_xcp:
    st.header("📚 Catalogo Nazionale e Aziendale dei Corsi Disponibili")
    st.caption("Prontuario degli eventi formativi accreditati. I codici di riferimento sono sincronizzati con il sistema di gestione del personale.")
    
    categorie_disponibili = ["Tutti", "Formazione Obbligatoria / Emergenza", "Sicurezza / Risk Management", "Igiene / Controllo Infezioni", "Informatica / Aspetti Legali"]
    categoria_scelta = st.selectbox("Seleziona Area Tematica:", categorie_disponibili)
    
    ricerca_xcp = st.text_input("Filtra rapidamente per titolo, codice REF o parole chiave:", key="search_xcp")
    
    prodotti_filtrati = []
    for item in STRUMENTARIO_XCP:
        match_categoria = (categoria_scelta == "Tutti") or (categoria_scelta in item["tipo"])
        match_ricerca = (ricerca_xcp.lower() in item["nome"].lower()) or (ricerca_xcp.lower() in item["ref"].lower()) or (ricerca_xcp.lower() in item["descrizione"].lower())
        
        if match_categoria and match_ricerca:
            prodotti_filtrati.append(item)
            
    if not prodotti_filtrati:
        st.warning("Nessun corso risponde ai criteri di ricerca impostati.")
    else:
        for item in prodotti_filtrati:
            with st.container():
                col_img, col_info = st.columns([1, 4])
                
                with col_img:
                    st.image(item["immagine"], caption=f"ID {item['ref']}", use_container_width=True)
                
                with col_info:
                    st.subheader(item["nome"])
                    c1, c2, c3 = st.columns(3)
                    c1.metric(label="Codice Evento ECM", value=item["ref"])
                    c2.metric(label="Macro Area", value=item["tipo"].split(" / ")[0])
                    c3.markdown(f"📍 **Sede di Svolgimento:**\n`{item['ambulatorio']}`")
                    
                    st.markdown(f"📝 **Programma e Obiettivi Didattici:** {item['descrizione']}")
                
                st.markdown("---")

# --- TAB 3: REGISTRO PRESENZE ---
with tab_lavaggio:
    st.header("✍️ Registro Sessione e Tracciabilità Partecipanti")
    st.caption("Modulo elettronico integrativo per la validazione della frequenza d'aula e la verbalizzazione dell'esito della prova finale.")
    
    col_form, col_data = st.columns([1, 2])
    
    with col_form:
        st.subheader("Registra Presenza / Test")
        with st.form("form_lavaggio", clear_on_submit=True):
            operatore = st.text_input("Nome e Cognome Dipendente:", placeholder="es. Dott. Rossi Mario")
            tipo_strumento = st.selectbox("Corso Selezionato:", [item["nome"] for item in STRUMENTARIO_XCP] + ["Corso Antincendio Rischio Elevato", "Primo Soccorso Aziendale"])
            metodo = st.radio("Profilo Professionale:", ["Personale Infermieristico", "Personale Medico", "Operatore Socio Sanitario (OSS)", "Personale Amministrativo"])
            esito = st.selectbox("Esito Prova di Apprendimento Finale:", ["Idoneo (Test Superato >= 75%)", "Non Idoneo (Test fallito - Da ripetere)", "Assente alla prova di verifica"])
            note = st.text_area("Note del Tutor / Giustificativi Orari:", placeholder="Es: Allontanatosi dall'aula dalle 11:00 alle 11:30 per urgenza di servizio.")
            
            submit = st.form_submit_button("Salva ed Archivia nel Registro")
            
            if submit:
                if operatore.strip() == "":
                    st.error("Errore di validazione: specificare il nominativo del dipendente per completare la registrazione.")
                else:
                    nuovo_record = {
                        "Data/Ora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Operatore": operatore,
                        "Corso / ID Evento": tipo_strumento,
                        "Ruolo": metodo,
                        "Esito Test": esito,
                        "Note": note
                    }
                    st.session_state.registro_presenze = pd.concat([
                        pd.DataFrame([nuovo_record]), st.session_state.registro_presenze
                    ], ignore_index=True)
                    st.success("Presenza archiviata con successo nel sistema.")
                    
    with col_data:
        st.subheader("Tracciato Log dei Partecipanti Registrati")
        if st.session_state.registro_presenze.empty:
            st.info("Nessun operatore inserito nel registro d'aula per la sessione corrente.")
        else:
            st.dataframe(st.session_state.registro_presenze, use_container_width=True)
            
            csv_data = st.session_state.registro_presenze.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Scarica File di Esportazione per Agenas (CSV)",
                data=csv_data,
                file_name=f"export_ecm_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# --- TAB 4: REGOLAMENTO ECM ---
with tab_procedura:
    st.header("📖 Quadro Normativo e Linee Guida di Riferimento")
    st.caption("Consultazione delle direttive per l'erogazione della formazione continua in ambito sanitario.")
    
    st.markdown(f"### {PROCEDURE_CARD['titolo']}")
    
    c_cod, c_resp = st.columns(2)
    c_cod.markdown(f"**Identificativo Procedura:** `{PROCEDURE_CARD['codice']}`")
    c_resp.markdown(f"**Ufficio Garante del Flusso:** {PROCEDURE_CARD['responsabile']}")
    
    st.markdown("#### 🎯 Obiettivi di Qualità del Sistema")
    for ob in PROCEDURE_CARD["obiettivi"]:
        st.markdown(f"- {ob}")
        
    st.markdown("#### 🗺️ Fasi del Processo di Validazione")
    for fase in PROCEDURE_CARD["fasi"]:
        with st.expander(fase["fase"], expanded=True):
            st.write(fase["dettaglio"])
            
    st.error(PROCEDURE_CARD["alert_sicurezza"])
