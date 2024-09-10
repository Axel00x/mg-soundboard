# mg-soundboard - 100% Gratuita

Benvenuto nel progetto **Soundboard**! Questa applicazione è una soundboard gratuita e personalizzabile che ti consente di gestire e riprodurre file audio tramite scorciatoie da tastiera. È progettata per essere semplice da usare e altamente configurabile.

## Funzionalità

- **Gestione dei Suoni**: Aggiungi, rimuovi e modifica i suoni con facilità.
- **Scorciatoie da Tastiera**: Assegna e modifica scorciatoie da tastiera per ogni suono.
- **Impostazioni Personalizzabili**:
  - **Loop**: Imposta se il suono deve essere ripetuto in loop.
  - **Stop Other Sounds**: Scegli se fermare altri suoni quando questo suono viene riprodotto (di default True).
  - **Volume**: Regola il volume del suono (default 100%).
  - **Active**: Abilita o disabilita il suono.
- **Scorciatoie Globali**: Attiva o disattiva la funzionalità di scorciatoia globale.
- **Salvataggio Configurazione**: Le impostazioni e i suoni vengono salvati automaticamente e ripristinati alla riapertura dell'applicazione.

## Installazione

1. **Clona il Repository**:

    ```bash
    git clone https://github.com/Axel00x/mg-soundboard.git
    cd soundboard
    ```

2. **Installa le Dipendenze**:

    Assicurati di avere Python 3.x installato, poi esegui:

    ```bash
    pip install -r requirements.txt
    ```

    Il file `requirements.txt` contiene tutte le librerie necessarie:
    - `pygame`
    - `tkinter`
    - `keyboard`

## Uso

1. **Avvia l'Applicazione**:

    ```bash
    python main.py
    ```

2. **Interfaccia Utente**:

    - **Aggiungi Suono**: Clicca sul pulsante "Aggiungi Suono" per caricare un file audio `.wav` e assegnargli una scorciatoia.
    - **Rimuovi Suono**: Seleziona un suono dalla lista e clicca "Rimuovi Suono".
    - **Modifica Suono**: Fai doppio clic su un suono nella lista per aprire una finestra di modifica.
    - **Impostazioni**: Modifica le impostazioni come nome, scorciatoia, loop, stop altri suoni, volume e stato attivo del suono.

3. **Scorciatoie da Tastiera**:

    - **Riproduzione Suono**: Premi il tasto associato al suono per riprodurlo.
    - **Stop Tutti i Suoni**: Premi il tasto `e` per fermare tutti i suoni in riproduzione.

4. **Impostazioni Generali**:

    - **Shortcut**: Attiva o disattiva la funzionalità di scorciatoia globale tramite una checkbox nella finestra principale.

## Configurazione

Le impostazioni vengono salvate automaticamente in un file chiamato `config.json` nella stessa directory del progetto. Le modifiche apportate durante l'uso vengono applicate e salvate in tempo reale.

## Contribuire

Se desideri contribuire al progetto, sentiti libero di aprire una pull request o segnalare problemi tramite il [sistema di issue di GitHub](https://github.com/Axel00x/mg-soundboard/issues).

## Licenza

Questo progetto è distribuito sotto la [Licenza MIT](LICENSE). È completamente gratuito e aperto a miglioramenti da parte della comunità.

## Contatti

Per qualsiasi domanda o supporto, puoi contattare l'autore del progetto all'indirizzo email: `tuo.email@example.com`.

---

Grazie per aver utilizzato **mg-soundboard**! Spero che questa applicazione ti sia utile e che tu possa godere della personalizzazione e delle funzionalità offerte.
