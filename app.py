import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# CONFIGURAZIONE PAGINA
# ==========================================
st.set_page_config(
    page_title="Hub Gestione Ambulatorio - databUSL",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DATABASE STATICI (STRUMENTARIO & LINEE GUIDA)
# ==========================================
STRUMENTARIO_XCP = [
    {
        "ref": "850011",
        "nome": "Pinza di Hartman Nasale (Standard)",
        "tipo": "Chirurgia / Pinze",
        "descrizione": "Strumento chirurgico articolato non da taglio, specifico per l'introduzione, la presa e la rimozione di tamponi, corpi estranei o frammenti ossei/tessutali nel distretto otorinolaringoiatrico (splancnocranio). Acciaio inossidabile medicale, autoclavabile a 134°C.",
        "immagine": "https://images.unsplash.com/photo-1579684389782-64d84b5e9053?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Ambulatorio 2 (ORL) - Armadio B1"
    },
    {
        "ref": "850022",
        "nome": "Miscelatore Automatico Polveri e Alginati",
        "tipo": "Materiali da Impronta / Protesi",
        "descrizione": "Dispositivo elettromeccanico per la miscelazione standardizzata, omogenea e priva di bolle d'aria di alginati per impronte dentali stabili. Riduce drasticamente l'errore umano nell'impasto manuale. Alimentazione 230V, ciclo rapido 12 secondi.",
        "immagine": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Ambulatorio 1 (Odontoiatria) - Ripiano Tecnico"
    },
    {
        "ref": "850033",
        "nome": "Kit Centratori XCP Rinn (Completo)",
        "tipo": "Diagnostica XCP",
        "descrizione": "Sistema universale di posizionamento per radiografie endorali con tecnica dei piani paralleli. Include bracci indicatori metallici, anelli di mira in plastica radiopaca colorata (Giallo=Posteriore, Blu=Anteriore, Rosso=Bitewing, Verde=Endodonzia) e blocchetti di morso.",
        "immagine": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Sterilizzazione / Stoccaggio RX"
    },
    {
        "ref": "850044",
        "nome": "Composito Fluido Fluoro-Rilasciante A2",
        "tipo": "Conservativa e Restaurativa",
        "descrizione": "Resina composita microibrida a bassa viscosità (flowable), siringa da 2g con ago applicatore. Indicata per restauri di Classe V, sigillature di solchi estesi e come liner cavitario. Fotopolimerizzabile a spettro standard (450-470 nm).",
        "immagine": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Ambulatorio 1 (Odontoiatria) - Cassetto C3"
    },
    {
        "ref": "850055",
        "nome": "File Endodontici NiTi Rotanti - Mtwo Assortiti",
        "tipo": "Endodonzia / Trattamento Canalare",
        "descrizione": "Strumenti endodontici rotanti in Nichel-Titanio a conicità variabile per la sagomatura meccanica del canale radicolare. Blister sterile da 6 pezzi (misure 10/.04, 15/.05, 20/.06, 25/.06). Utilizzo consigliato con motore endodontico a controllo di torque.",
        "immagine": "https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?auto=format&fit=crop&q=80&w=200",
        "ambulatorio": "Ambulatorio 1 (Odontoiatria) - Mobiletto Endodonzia"
    }
]

PROCEDURE_CARD = {
    "titolo": "Linee Guida di Allestimento e Tracciabilità dei Campioni Biologici in Chirurgia Ambulatoriale",
    "codice": "LG-INF-SURG-042-REV03",
    "ambulatori": ["Ambulatorio 1 (Chirurgia/Odontoiatria)", "Ambulatorio 2 (ORL)"],
    "responsabile": "Coordinatore Infermieristico / Infermiere di Sala",
    "obiettivi": [
        "Garantire l'identità univoca del paziente sul contenitore del pezzo anatomo-patologico.",
        "Prevenire la degradazione dei tessuti biologici mediante fissazione standardizzata.",
        "Assicurare la corretta catena di custodia e tracciabilità informatica sul registro cartaceo e digitale dell'Azienda Sanitaria."
    ],
    "fasi": [
        {"fase": "1. Identificazione", "dettaglio": "Al momento del prelievo tissutale, stampare l'etichetta bar-code davanti al paziente. Verificare verbalmente Cognome, Nome e Data di Nascita. Applicare l'etichetta sul CORPO del contenitore, MAI sul tappo."},
        {"fase": "2. Fissazione", "dettaglio": "Immergere immediatamente il campione in Formalina Tamponata al 10% (Rapporto volume fissativo/tessuto ottimale 10:1). Chiudere ermeticamente. Annotare l'ora esatta di immersione per i tessuti speciali."},
        {"fase": "3. Registrazione", "dettaglio": "Compilare la richiesta d'esame istologico su portale aziendale. Riportare sul registro di ambulatorio: Numero Progressivo interno, Nome Paziente, Tipo di Tessuto, Quesito Clinico, Firma dell'operatore che effettua il confezionamento."},
        {"fase": "4. Logistica e Trasporto", "dettaglio": "Inserire il contenitore nel sacchetto secondario per il rischio biologico (con tasca separata per i documenti). Custodire nel frigorifero dedicato a +4°C fino al ritiro programmato da parte del servizio di trasporto aziendale verso l'Anatomia Patologica."}
    ],
    "alert_sicurezza": "⚠️ ATTENZIONE: La formalina è un cancerogeno accertato (H350). Manipolare tassativamente sotto cappa aspirante o in locali perfettamente ventilati indossando DPI idonei (guanti in nitrile a polsino lungo, visiera paraschizzi e mascherina FFP3). In caso di sversamento accidentale, utilizzare l'apposito kit di assorbimento con granuli neutralizzanti presente nell'Ambulatorio 2."
}

# ==========================================
# STATO DELL'APPLICAZIONE (SESSION STATE)
# ==========================================
if "registro_lavaggio" not in st.session_state:
    st.session_state.registro_lavaggio = pd.DataFrame(columns=[
        "Data/Ora", "Operatore", "Tipo Strumento", "Metodo Lavaggio", "Esito Visivo", "Note"
    ])

if "checklist_apertura" not in st.session_state:
    st.session_state.checklist_apertura = {
        "Accensione Riuniti e Compressore": False,
        "Controllo Scadenze Sterilizzazione": False,
        "Verifica Carrello Emergenza (Defibrillatore/Farmaci)": False,
        "Caricamento Autoclave e Test (Helix/Vacuum)": False,
        "Check-up Soluzioni Disinfettanti (Linee Idriche e Vasche)": False
    }

# ==========================================
# INTERFACCIA UTENTE PRINCIPALE
# ==========================================
st.title("🏥 databUSL - Hub Digitale delle Procedure Infermieristiche")
st.subheader("Piattaforma di Tracciabilità, Logistica Clinica e Controllo Operativo Ambulatoriale")
st.markdown("---")

# Layout a schede per suddividere nettamente le macro-funzionalità dell'ambulatorio
tab_check, tab_xcp, tab_lavaggio, tab_procedura = st.tabs([
    "📋 CHECKLIST APERTURA", 
    "🛠️ PRONTUARIO STRUMENTI/XCP", 
    "🧼 TRACCIABILITÀ LAVAGGIO", 
    "📖 MANUALE PROCEDURE"
])

# --- TAB 1: CHECKLIST DI APERTURA MATTUTINA ---
with tab_check:
    st.header("📋 Controlli Obbligatori di Inizio Turno Mattutino")
    st.caption("La spunta dei seguenti parametri assicura la conformità ai requisiti di sicurezza clinica e tecnologica prima dell'accesso dei pazienti.")
    
    col_check, col_status = st.columns([2, 1])
    
    with col_check:
        completati = 0
        for task in st.session_state.checklist_apertura.keys():
            # Mostra checkbox persistenti legati al session state
            st.session_state.checklist_apertura[task] = st.checkbox(task, value=st.session_state.checklist_apertura[task])
            if st.session_state.checklist_apertura[task]:
                completati += 1
                
    with col_status:
        totale_task = len(st.session_state.checklist_apertura)
        percentuale = int((completati / totale_task) * 100)
        
        st.metric(label="Task Completati", value=f"{completati} / {totale_task}", delta=f"{percentuale}%")
        st.progress(completati / totale_task)
        
        if completati == totale_task:
            st.success("✅ Ambulatorio conforme! Tutti i dispositivi e i sistemi di sicurezza sono operativi per l'attività clinica.")
        else:
            st.warning("⚠️ Presenza di task non completati. Completare le verifiche prima dell'inizio delle attività chirurgiche o diagnostiche.")

# --- TAB 2: PRONTUARIO STRUMENTI E MATERIALI (ESPANSO E DETTAGLIATO) ---
with tab_xcp:
    st.header("🛠️ Registro e Tracciabilità Materiali, Chirurgia e Protesi")
    st.caption("Prontuario ufficiale per il controllo e l'identificazione dei dispositivi medici. Codici a 6 cifre allineati con l'anagrafica di magazzino.")
    
    # Filtri di Categoria per facilitare la consultazione del mega database
    categorie_disponibili = ["Tutti", "Chirurgia / Pinze", "Materiali da Impronta / Protesi", "Diagnostica XCP", "Conservativa e Restaurativa", "Endodonzia / Trattamento Canalare"]
    categoria_scelta = st.selectbox("Seleziona Categoria Merceologica:", categorie_disponibili)
    
    ricerca_xcp = st.text_input("Filtra rapidamente per nome, REF o descrizione:", key="search_xcp")
    
    # Filtraggio logico dei prodotti
    prodotti_filtrati = []
    for item in STRUMENTARIO_XCP:
        match_categoria = (categoria_scelta == "Tutti") or (categoria_scelta in item["tipo"])
        match_ricerca = (ricerca_xcp.lower() in item["nome"].lower()) or (ricerca_xcp.lower() in item["ref"].lower()) or (ricerca_xcp.lower() in item["descrizione"].lower())
        
        if match_categoria and match_ricerca:
            prodotti_filtrati.append(item)
            
    if not prodotti_filtrati:
        st.warning("Nessun articolo trovato nel prontuario con i filtri inseriti.")
    else:
        for item in prodotti_filtrati:
            with st.container():
                col_img, col_info = st.columns([1, 4])
                
                with col_img:
                    st.image(item["immagine"], caption=f"REF {item['ref']}", use_container_width=True)
                
                with col_info:
                    st.subheader(item["nome"])
                    c1, c2, c3 = st.columns(3)
                    c1.metric(label="Codice Articolo Gerhò", value=item["ref"])
                    c2.metric(label="Macro Categoria", value=item["tipo"].split(" / ")[0])
                    c3.markdown(f"📍 **Ubicazione:**\n`{item['ambulatorio']}`")
                    
                    st.markdown(f"📝 **Dettaglio Clinico e Specifiche Tecniche:** {item['descrizione']}")
                
                st.markdown("---")

# --- TAB 3: TRACCIABILITÀ LAVAGGIO E DECONTAMINAZIONE STRUMENTARIO ---
with tab_lavaggio:
    st.header("🧼 Registro Validazione Decontaminazione e Termodisinfezione")
    st.caption("Modulo normativo per la tracciabilità delle fasi pre-sterilizzazione dello strumentario riutilizzabile (D.Lgs 81/08 e linee guida ISPESL).")
    
    col_form, col_data = st.columns([1, 2])
    
    with col_form:
        st.subheader("Registra Nuovo Ciclo")
        with st.form("form_lavaggio", clear_on_submit=True):
            operatore = st.text_input("Iniziali Operatore / ID Cartellino:", placeholder="es. IP Rossi M.")
            tipo_strumento = st.selectbox("Tipologia Dispositivo:", [item["nome"] for item in STRUMENTARIO_XCP] + ["Kit Esame Base Odontoiatrico", "Specula Auricolari ORL", "Turbine/Manipoli"])
            metodo = st.radio("Metodo di Trattamento:", ["Termodisinfettore Automatico (Ciclo P1)", "Ultrasuoni + Lavaggio Manuale", "Decontaminazione Chimica Manuale (Acido Peracetico)"])
            esito = st.selectbox("Esito Ispezione Visiva post-lavaggio:", ["Superato (Strumento Integro e Pulito)", "Non Superato (Presenza residui - Ripetere ciclo)", "Non Superato (Strumento ossidato/danneggiato - Ritiro)"])
            note = st.text_area("Note Tecniche / Lotto Soluzione Disinfettante:", placeholder="Es: Lotto Peracetico X123, nessun residuo metallico.")
            
            submit = st.form_submit_button("Archivia e Firma Record")
            
            if submit:
                if operatore.strip() == "":
                    st.error("Impossibile salvare: è necessario specificare l'operatore per la firma del record.")
                else:
                    nuovo_record = {
                        "Data/Ora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Operatore": operatore,
                        "Tipo Strumento": tipo_strumento,
                        "Metodo Lavaggio": metodo,
                        "Esito Visivo": esito,
                        "Note": note
                    }
                    st.session_state.registro_lavaggio = pd.concat([
                        pd.DataFrame([nuovo_record]), st.session_state.registro_lavaggio
                    ], ignore_index=True)
                    st.success("Record registrato e inserito nel database temporaneo corrente.")
                    
    with col_data:
        st.subheader("Giornale di Bordo Ambulatoriale (Cicli Odierni)")
        if st.session_state.registro_lavaggio.empty:
            st.info("Nessun ciclo di lavaggio registrato nelle ultime 24 ore. Utilizza il modulo a sinistra per inserire i dati.")
        else:
            st.dataframe(st.session_state.registro_lavaggio, use_container_width=True)
            
            # Funzione di esportazione CSV rapida per controlli interni o audit di reparto
            csv_data = st.session_state.registro_lavaggio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Esporta Registro in CSV / Excel",
                data=csv_data,
                file_name=f"registro_lavaggio_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# --- TAB 4: MANUALE PROCEDURE ED ALLINEAMENTO NORMATIVO ---
with tab_procedura:
    st.header("📖 Manuale Operativo di Reparto")
    st.caption("Visualizzazione delle schede di procedura standardizzate per l'addestramento e l'allineamento del personale infermieristico.")
    
    st.markdown(f"### {PROCEDURE_CARD['titolo']}")
    
    c_cod, c_resp = st.columns(2)
    c_cod.markdown(f"**Codice Documento:** `{PROCEDURE_CARD['codice']}`")
    c_resp.markdown(f"**Professionista Responsabile dell'Applicazione:** {PROCEDURE_CARD['responsabile']}")
    
    st.markdown("#### 🎯 Obiettivi Clinico-Assistenziali")
    for ob in PROCEDURE_CARD["obiettivi"]:
        st.markdown(f"- {ob}")
        
    st.markdown("#### 🗺️ Sequenza Cronologica delle Attività")
    for fase in PROCEDURE_CARD["fasi"]:
        with st.expander(fase["fase"], expanded=True):
            st.write(fase["dettaglio"])
            
    st.error(PROCEDURE_CARD["alert_sicurezza"])
