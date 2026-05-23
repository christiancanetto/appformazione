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

# 3. CATALOGO MASSIVO DEI MATERIALI E STRUMENTARIO (Codici Articolo reali Gerhò / Specialistica)
STRUMENTARIO_XCP = [
    # --- SEZIONE DIAGNOSTICA XCP ---
    {
        "nome": "Kit Completo Posizionatori XCP Rinn Evolution",
        "ref": "542001",
        "tipo": "Diagnostica XCP",
        "ambulatorio": "Area Diagnostica / Radiologia (Tutti gli studi)",
        "descrizione": "Kit completo per l'allineamento radiografico endorale con tecnica del parallelismo. Include bracci metallici, anelli di mira e blocchetti di morso. Autoclavabili.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Posizionatore XCP Rinn Anteriore - Colore Blu",
        "ref": "542002",
        "tipo": "Diagnostica XCP",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica",
        "descrizione": "Componenti specifici per i settori anteriori (incisivi e canini). L'anello di mira blu e l'indicatore centrano il fascio radiogeno perpendicolarmente all'asse lungo del dente.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Posizionatore XCP Rinn Posteriore - Colore Giallo",
        "ref": "542003",
        "tipo": "Diagnostica XCP",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica",
        "descrizione": "Componenti specifici per i settori posteriori (molari e premolari). Ottimizza l'allineamento geometrico orizzontale riducendo le sovrapposizioni delle corone.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },
    {
        "nome": "Posizionatore XCP Rinn Bitewing - Colore Rosso",
        "ref": "542004",
        "tipo": "Diagnostica XCP",
        "ambulatorio": "Ambulatorio di Radiologia e Diagnostica",
        "descrizione": "Specifico per radiografie interprossimali per la ricerca di carie e controllo delle creste ossee marginali. Mostra contemporaneamente corone superiori e inferiori.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Posizionatore XCP Rinn Endodontico - Colore Verde",
        "ref": "542005",
        "tipo": "Diagnostica XCP",
        "ambulatorio": "Ambulatorio di Endodonzia e Conservativa",
        "descrizione": "Disegnato appositamente con una struttura scavata per aggirare la diga di gomma, i file (aghi endodontici) o i pin intracanalari inseriti senza spostare il sensore.",
        "immagine": "https://i.ebayimg.com/images/g/k3UAAeSwKOdp~sVg/s-l400.jpg"
    },

    # --- SEZIONE PINZE DA ESTRAZIONE (CHIRURGIA) ---
    {
        "nome": "Pinza per Incisivi e Canini Superiori Fig. 1",
        "ref": "110001",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Pinza chirurgica con becchi diritti, non toccantisi, specifica per l'avulsione di elementi monoradicolati dell'arcata superiore (da canino a canino).",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Premolari Superiori Fig. 7",
        "ref": "110007",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Pinza con leggera curvatura a S del manico per favorire l'accesso posteriore. Becchi simmetrici adatti all'anatomia dei premolari superiori.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Molari Superiori Destri Fig. 17",
        "ref": "110017",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Pinza asimmetrica. Presenta una punta sporgente sul becco vestibolare creata appositamente per adattarsi alla biforcazione delle radici vestibolari dei molari superiori del quadrante di destra (1.6 - 1.7 - 1.8).",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Molari Superiori Sinistri Fig. 18",
        "ref": "110018",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Pinza asimmetrica speculare alla 17. La punta sul becco vestibolare è posizionata per alloggiare la biforcazione radicolare dei molari superiori del quadrante di sinistra (2.6 - 2.7 - 2.8).",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Radici Superiori (Baionetta) Fig. 51",
        "ref": "110051",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Forma a baionetta accentuata con becchi molto sottili e toccantisi. Consente l'estrazione profonda di residui radicolari nell'arcata superiore senza ledere l'alveolo.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Incisivi e Radici Inferiori Fig. 4",
        "ref": "110004",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Pinza ad angolo retto (90°) rispetto al manico, con becchi stretti e paralleli, ottimizzata per gli elementi monoradicolati e frammenti inferiori anteriori.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Premolari Inferiori Fig. 13",
        "ref": "110013",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Inclinazione a 90°, becchi più larghi e arrotondati rispetto alla Fig. 4, non toccantisi a riposo, ideale per la presa sulla corona sferica dei premolari inferiori.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Molari Inferiori (Becco di Falco) Fig. 22",
        "ref": "110022",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Pinza a 'Becco di Falco'. Entrambi i becchi terminano con una punta pronunciata per ghermire la biforcazione delle radici (mesiale e distale) dei molari inferiori sia destri che sinistri.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Pinza per Terzi Molari Inferiori Fig. 79",
        "ref": "110079",
        "tipo": "Strumentario Chirurgico / Pinze",
        "ambulatorio": "Chirurgia / Sale Cliniche",
        "descrizione": "Becchi corti e fortemente inclinati verso l'operatore per permettere l'apertura e l'azione negli spazi ristretti del trigono retro-molare inferiore.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },

    # --- SEZIONE PROTESI E IMPRONTE ---
    {
        "nome": "Alginato Idrocolloide Irreversibile ad Alta Precisione",
        "ref": "320110",
        "tipo": "Materiali da Impronta / Protesi",
        "ambulatorio": "Laboratorio Protesi / Studi Clinici",
        "descrizione": "Alginato di classe A a viraggio cromatico di fase. Ottima stabilità dimensionale (fino a 100 ore). Indicato per modelli di studio, antagonisti e protesi mobile temporanea.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Silicone per Addizione Putty Soft (Base + Catalizzatore)",
        "ref": "320220",
        "tipo": "Materiali da Impronta / Protesi",
        "ambulatorio": "Laboratorio Protesi / Studi Clinici",
        "descrizione": "Polivinilsilossano (PVS) ad alta viscosità per la prima impronta (tecnica della doppia impronta o della doppia miscelazione). Idrocompatibile, durezza finale ottimale.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Silicone per Addizione Light Body - Cartucce",
        "ref": "320225",
        "tipo": "Materiali da Impronta / Protesi",
        "ambulatorio": "Laboratorio Protesi / Studi Clinici",
        "descrizione": "Polivinilsilossano a bassissima viscosità (fluido leggero) da estrudere direttamente nel solco gengivale tramite siringa o dispenser. Massima precisione sui margini di preparazione protesica.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Punta Miscelatrice Gialla per Fluide PVS (Conf. da 50)",
        "ref": "320912",
        "tipo": "Consumabile di Reparto",
        "ambulatorio": "Magazzino / Studi Clinici",
        "descrizione": "Punte di miscelazione dinamico-passiva per cartucce di materiale fluido da impronta. Assicurano un'estrusione omogenea senza bolle d'aria.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Adesivo Universale per Portaimpronte in Plastica/Metallo",
        "ref": "320340",
        "tipo": "Materiali da Impronta / Protesi",
        "ambulatorio": "Laboratorio Protesi / Studi Clinici",
        "descrizione": "Soluzione liquida da stendere sui bordi del portaimpronte prima del caricamento del silicone, per evitare il distacco del materiale durante la rimozione dal cavo orale.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },

    # --- SEZIONE CONSERVATIVA E RESTAURATIVA ---
    {
        "nome": "Composito Microibrido Universale Enamel EnA HRi (Siringa A2)",
        "ref": "220402",
        "tipo": "Conservativa e Restaurativa",
        "ambulatorio": "Conservativa / Estetica",
        "descrizione": "Composito fotopolimerizzabile ad alto indice di rifrazione biologica. Siringa da 5g colore smalto/dentina A2. Lucidabilità eccellente.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Gel Mordenzante Acido Ortofosforico 37% (Siringa Jumbo)",
        "ref": "220101",
        "tipo": "Conservativa e Restaurativa",
        "ambulatorio": "Conservativa / Estetica",
        "descrizione": "Gel tixotropico blu per la condizionatura di smalto (30 sec) e dentina (15 sec). Lavaggio rapido senza residui.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Adesivo Monocomponente Universale Prime&Bond Active",
        "ref": "220150",
        "tipo": "Conservativa e Restaurativa",
        "ambulatorio": "Conservativa / Estetica",
        "descrizione": "Adesivo universale attivo con controllo dell'umidità. Utilizzabile con tecniche Etch&Rinse, Self-Etch o Selective Etch. Riduce la sensibilità post-operatoria.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },

    # --- SEZIONE ENDODONZIA ---
    {
        "nome": "File Endodontici Rotanti Protaper Gold F1 (25mm Lg)",
        "ref": "410321",
        "tipo": "Endodonzia / Trattamento Canalare",
        "ambulatorio": "Ambulatorio di Endodonzia",
        "descrizione": "Strumenti rotanti in Nichel-Titanio con trattamento termico Gold. Flessibilità migliorata per la sagomatura dei canali radicolari curvi e complessi.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },
    {
        "nome": "Coni di Guttaperca Calibrati Protaper Gold F1",
        "ref": "410501",
        "tipo": "Endodonzia / Trattamento Canalare",
        "ambulatorio": "Ambulatorio di Endodonzia",
        "descrizione": "Coni di guttaperca per l'otturazione tridimensionale del canale radicolare, con conicità perfettamente corrispondente al file di sagomatura F1.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },

    # --- SEZIONE IGIENE E PROFILASSI ---
    {
        "nome": "Pasta Profilassi Detartrina Plus con Fluoro (Tubetto 40g)",
        "ref": "610200",
        "tipo": "Igiene e Profilassi",
        "ambulatorio": "Studio Igiene Orale",
        "descrizione": "Pasta abrasiva specifica per la lucidatura post-detartrasi. Rimuove efficacemente macchie estrinseche (caffè, fumo) rilasciando fluoro protettivo.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    },

    # --- SEZIONE STERILIZZAZIONE E DISINFEZIONE ---
    {
        "nome": "Disinfettante Spray Rapido Zeta 3 Wipes Total",
        "ref": "710115",
        "tipo": "Igiene e Disinfezione",
        "ambulatorio": "Area Sterilizzazione / Tutti gli studi",
        "descrizione": "Salviette umidificate detergenti e disinfettanti ad ampio spettro d'azione (battericida, lieviticida, tubercolocida, virucida) per superfici di dispositivi medici non invasivi.",
        "immagine": "https://static.wixstatic.com/media/45eb7b_585772237ea4419b910cfdb58a441178~mv2.png/v1/fit/w_500,h_500,q_90/file.png"
    }
]

# 4. POOL DI DOMANDE PER IL SISTEMA DI GAMIFICATION (Linee Guida Generali)
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
    st.session_state["tipo_quiz"] = "" # 'testo' o 'riconoscimento'

# Funzioni di supporto
def elimina_commento(procedura, indice):
    st.session_state["commenti"][procedura].pop(indice)

def vota_up(procedura):
    st.session_state["voti"][procedura]["up"] += 1

def vota_down(procedura):
    st.session_state["voti"][procedura]["down"] += 1

# FUNZIONE SPERIMENTALE: Generatore dinamico di quiz di riconoscimento prodotti
def genera_quiz_riconoscimento_prodotti():
    domande = []
    pool_materiali = STRUMENTARIO_XCP.copy()
    random.shuffle(pool_materiali)
    
    # Seleziona fino a 5 materiali diversi per creare il mini-test
    for mat in pool_materiali[:5]:
        tipo_test = random.choice(["codice", "indicazione", "chirurgia_specifica"])
        
        if tipo_test == "codice":
            # Chiedi di indovinare il codice REF corretto
            altri_ref = [m["ref"] for m in STRUMENTARIO_XCP if m["ref"] != mat["ref"]]
            opzioni = random.sample(altri_ref, 2) + [mat["ref"]]
            random.shuffle(opzioni)
            domande.append({
                "domanda": f"Qual è il Codice Articolo Gerhò corretto per il seguente prodotto: '{mat['nome']}'?",
                "opzioni": opzioni,
                "corretta": mat["ref"]
            })
        elif tipo_test == "indicazione":
            # Chiedi di associare la descrizione d'uso corretta
            altre_desc = [m["descrizione"] for m in STRUMENTARIO_XCP if m["descrizione"] != mat["descrizione"]]
            opzioni = random.sample(altre_desc, 2) + [mat["descrizione"]]
            random.shuffle(opzioni)
            domande.append({
                "domanda": f"Identifica la specifica clinica e l'indicazione d'uso corretta per l'articolo '{mat['nome']}':",
                "opzioni": opzioni,
                "corretta": mat["descrizione"]
            })
        else:
            # Chiedi di indovinare il nome del prodotto partendo dal codice articolo
            altri_nomi = [m["nome"] for m in STRUMENTARIO_XCP if m["nome"] != mat["nome"]]
            opzioni = random.sample(altri_nomi, 2) + [mat["nome"]]
            random.shuffle(opzioni)
            domande.append({
                "domanda": f"A quale specifico presidio o pinza odontoiatrica corrisponde il Codice Articolo Gerhò '{mat['ref']}'?",
                "opzioni": opzioni,
                "corretta": mat["nome"]
            })
    return domande

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

    st.title("🦷 Hub Operativo e Linee Guida di Studio - databUSL")
    
    # --- ASSISTENTE AI DI REPARTO POTENZIATO ---
    st.markdown("---")
    with st.container():
        st.markdown("### 🤖 Assistente AI - Supporto Decisionale Clinico ed Inventariale")
        st.caption("L'Intelligenza Artificiale analizza istantaneamente i protocolli, le pinze estrattive e l'intero inventario protesico/conservativo.")
        
        query_ai = st.text_input("Inserisci codice articolo, nome materiale o quesito clinico (es. '110022', 'alginato', 'becco di falco'):", placeholder="Chiedi all'AI...")
        
        if query_ai:
            query_clean = query_ai.lower().strip()
            risposta_trovata = False
            
            # Scansione inventario materiali completo
            for xcp in STRUMENTARIO_XCP:
                if query_clean in xcp["nome"].lower() or query_clean in xcp["ref"].lower() or query_clean in xcp["descrizione"].lower():
                    st.markdown(f"**🤖 Risposta dell'Assistente AI (Riscontro Catalogo ed Inventario):**")
                    st.success(f"Trovata corrispondenza esatta nel database di reparto:\n\n"
                               f"📦 **Articolo**: {xcp['nome']} (REF Catalogo: `{xcp['ref']}`)\n"
                               f"🗂️ **Classificazione**: {xcp['tipo']}\n"
                               f"📍 **Destinazione di Reparto**: {xcp['ambulatorio']}\n"
                               f"⚙️ **Specifiche d'uso cliniche**: {xcp['descrizione']}")
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
                st.warning("🤖 **Risposta dell'Assistente AI:** Nessuna corrispondenza esatta trovata per i criteri inseriti. Verifica di aver digitato correttamente il codice numerico a 6 cifre.")
                
    st.markdown("---")

    # Navigazione principale dei Tab dell'applicazione
    tab_procedure, tab_xcp, tab_mappa, tab_esercitati = st.tabs([
        "📋 Procedure Cliniche", 
        "🛠️ Prontuario Materiali e Strumenti", 
        "🗺️ Anatomia dell'Ambulatorio", 
        "🎯 Esercitati (Addestramento)"
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

    # --- TAB 2: PRONTUARIO STRUMENTI E MATERIALI (ESPANSO E DETTAGLIATO) ---
    with tab_xcp:
        st.header("🛠️ Registro e Tracciabilità Materiali, Chirurgia e Protesi")
        st.caption("Prontuario ufficiale per il controllo e l'identificazione dei dispositivi medici. Codici a 6 cifre allineati con l'anagrafica di magazzino.")
        
        # Filtri di Categoria per facilitare la consultazione del mega database
        categorie_disponibili = ["Tutti", "Chirurgia / Pinze", "Materiali da Impronta / Protesi", "Diagnostica XCP", "Conservativa e Restaurativa", "Endodonzia / Trattamento Canalare"]
        categoria_scelta = st.selectbox("Seleziona Categoria Merceologica:", categories_disponibili)
        
        ricerca_xcp = st.text_input("Filtra rapidamente per nome, REF o descrizione:", key="search_xcp")
        
        # Filtraggio logico dei prodotti
        prodotti_filtrati = []
        for item in STRUMENTARIO_XCP:
            match_categoria = (categoria_scelta == "Tutti") or (categoria_scelta in item["tipo"])
            match_ricerca = (ricerca_xcp.lower() in item["nome"].lower()) or (ricerca_xcp.lower() in item["ref"].lower()) or (ricerca_xcp.lower() in item["descrizione"].lower())
            
            if match_categoria and match_ricerca:
                prodotti_filtrati.append(item)
                
        if non prodotti_filtrati:
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

    # --- TAB 4: GAMIFICATION E AUTOVALUTAZIONE (POTENZIATO CON RICONOSCIMENTO PRODOTTI) ---
    with tab_esercitati:
        st.header("🎯 Addestramento e Gamification Avanzata")
        st.caption("Strumento critico per formare i nuovi assunti e il personale di studio. Rispondi correttamente per scalare la classifica interna del reparto.")
        
        col_quiz, col_classifica = st.columns([6, 4])
        
        with col_quiz:
            st.subheader("⚙️ Configura Sessione di Addestramento")
            
            if not st.session_state["quiz_attivo"]:
                st.write("Scegli la modalità di test adatta al tuo livello:")
                
                btn_argomento, btn_tutto, btn_riconoscimento = st.columns(3)
                
                with btn_argomento:
                    if st.button("📚 Teoria per Argomento", use_container_width=True):
                        argomento = random.choice(list(QUIZ_DATA.keys()))
                        st.session_state["domande_selezionate"] = QUIZ_DATA[argomento]
                        st.session_state["quiz_attivo"] = True
                        st.session_state["indice_domanda"] = 0
                        st.session_state["punteggio_sessione"] = 0
                        st.session_state["tipo_quiz"] = "teoria"
                        st.rerun()
                        
                with btn_tutto:
                    if st.button("🌐 Teoria Globale", use_container_width=True):
                        tutte_le_domande = []
                        for lista in QUIZ_DATA.values():
                            tutte_le_domande.extend(lista)
                        random.shuffle(tutte_le_domande)
                        st.session_state["domande_selezionate"] = tutte_le_domande
                        st.session_state["quiz_attivo"] = True
                        st.session_state["indice_domanda"] = 0
                        st.session_state["punteggio_sessione"] = 0
                        st.session_state["tipo_quiz"] = "teoria"
                        st.rerun()
                        
                with btn_riconoscimento:
                    if st.button("🔎 Riconoscimento Prodotti & REF", use_container_width=True):
                        # Generazione dinamica del quiz basata sul mega database dei materiali appena inserito
                        st.session_state["domande_selezionate"] = genera_quiz_riconoscimento_prodotti()
                        st.session_state["quiz_attivo"] = True
                        st.session_state["indice_domanda"] = 0
                        st.session_state["punteggio_sessione"] = 0
                        st.session_state["tipo_quiz"] = "riconoscimento"
                        st.rerun()
                        
                st.info("💡 **Consiglio per l'addestramento:** Utilizza la modalità *'Riconoscimento Prodotti & REF'* per padroneggiare la codifica del magazzino e velocizzare la preparazione dei vassoi chirurgici e protesici.")
            
            else:
                lista_domande = st.session_state["domande_selezionate"]
                attuale = st.session_state["indice_domanda"]
                
                if attuale < len(lista_domande):
                    dati_domanda = lista_domande[attuale]
                    st.markdown(f"📊 **Quesito {attuale + 1} di {len(lista_domande)}**")
                    
                    # Segnalatore visivo del tipo di quiz per l'utente
                    if st.session_state["tipo_quiz"] == "riconoscimento":
                        st.warning("🔍 **TEST DI RICONOSCIMENTO MATERIALI ED INVENTARIO**")
                    else:
                        st.info("📖 **TEST DI TEORIA E PROTOCOLLI CLINICI**")
                        
                    st.markdown(f"#### {dati_domanda['domanda']}")
                    
                    # Radio button per la scelta della risposta
                    risposta = st.radio("Seleziona l'opzione corretta:", dati_domanda["opzioni"], key=f"q_prod_{attuale}")
                    
                    if st.button("Conferma e Prosegui ➔", use_container_width=True):
                        if risposta == dati_domanda["corretta"]:
                            st.session_state["punteggio_sessione"] += 10
                            st.toast("Risposta Corretta! +10 Punti", icon="✅")
                        else:
                            st.toast(f"Risposta Errata! La risposta corretta era: {dati_domanda['corretta']}", icon="❌")
                        st.session_state["indice_domanda"] += 1
                        st.rerun()
                else:
                    st.success(f"🎉 Sessione completata con successo! Punteggio totale ottenuto in questo set: **+{st.session_state['punteggio_sessione']} PT**.")
                    nome_utente_attuale = USER_DB[st.session_state["username"]]["nome_completo"]
                    
                    # Aggiornamento persistente della classifica nel session_state
                    st.session_state["classifica"][nome_utente_attuale] += st.session_state["punteggio_sessione"]
                    
                    if st.button("Salva nel Registro di Reparto ed Esci", use_container_width=True):
                        st.session_state["quiz_attivo"] = False
                        st.session_state["tipo_quiz"] = ""
                        st.rerun()

        with col_classifica:
            st.subheader("🏆 Leaderboard di Studio")
            classifica_ordinata = sorted(st.session_state["classifica"].items(), key=lambda item: item[1], reverse=True)
            for posizione, (operatore, punti) in enumerate(classifica_ordinata, start=1):
                medaglia = "🥇" if posizione == 1 else "🥈" if posizione == 2 else "🥉" if posizione == 3 else "👤"
                nome_connesso = USER_DB[st.session_state["username"]]["nome_completo"]
                if operatore == nome_connesso:
                    st.markdown(f"**{medaglia} Posizione {posizione}: {operatore} — {punti} PT (Tu)** 🌟")
                else:
                    st.markdown(f"{medaglia} Posizione {posizione}: {operatore} — {punti} PT")
