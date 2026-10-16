# Atelier Yumia: Traduzione Italiana & Toolkit

[🇬🇧 Read in English](README.md) | [🇮🇹 Leggi in Italiano](README_IT.md)

---

Patch di traduzione amatoriale in lingua italiana al 100% per **Atelier Yumia: The Alchemist of Memories & the Envisioned Land** (Steam / PC).

Sostituisce lo slot lingua **Spagnolo (Español)** con un italiano naturale e completo.

---

## Installazione Rapida (1-Click)

### Requisiti
- Python 3.10+
- Gioco installato su Steam (PC)

### Procedura
1. Scarica o clona questo repository.
2. Fai doppio clic su **`run_toolkit.bat`** e premi **`[1]`** per installare la traduzione pronta al 100%.
3. Avvia il gioco e nelle impostazioni seleziona come lingua del testo: **Español**.

*Fatto! Tutti i dialoghi della storia, missioni, tutorial, oggetti, menu e interfaccia (UI) saranno in italiano.*

---

## Opzioni del Toolkit (`run_toolkit.bat`)

Avviando `run_toolkit.bat` (oppure `python src/yumia_cli.py`) si aprirà un menu interattivo:

- **`[1] Install / Update translation in game`**: Inietta automaticamente tutti i 29.007 testi tradotti nei file di gioco (~15 secondi, nessun costo API, pronto per giocare).
- **`[2] AI Translation`**: Procedura guidata per ritradurre o personalizzare i testi tramite Intelligenza Artificiale. *(Modello consigliato: **`gpt-6-luna`** via OpenAI — velocissimo, alta coerenza nei termini e costo inferiore a 0,50 $ per l'intero gioco).*
- **`[3] Extract raw texts from game`**: Estrae i testi originali direttamente dai file del gioco in un nuovo file JSON (utile in caso di futuri DLC o espansioni).
- **`[4] Change / Set game folder path`**: Mostra la cartella del gioco rilevata automaticamente e consente di impostarne una personalizzata se necessario.

---

## Aggiornamenti del Gioco / Patch di Steam

Se un aggiornamento ufficiale del gioco o una verifica dell'integrità dei file di Steam ripristina la lingua originale:
- Riapri semplicemente **`run_toolkit.bat`** e premi di nuovo **`[1]`** (o lancia `python src/update_patch.py`).
- Lo script ri-estrarrà e inietterà nuovamente la traduzione in circa 15 secondi.

---

## Struttura dei File

| File / Cartella | Descrizione |
| :--- | :--- |
| **`project_yumia_es_en.json`** | Dataset completo con tutti i 29.007 segmenti tradotti in italiano. |
| **`run_toolkit.bat`** | Launcher interattivo Windows (menu rapido a 1 clic). |
| **`src/yumia_cli.py`** | Wizard interattivo da terminale (installatore, configuratore IA, estrattore). |
| **`src/update_patch.py`** | Script automatizzato per installazione e repackaging rapido. |
| **`src/yumia_text_tool.py`** | Estrattore e iniettore per formati A26 EBM e UI `message.json`. |
| **`src/yumia_translate.py`** | Tool di traduzione IA concorrente multi-thread (OpenAI / Ollama / compatibili). |
| **`src/fix_accents.py`** | Normalizzatore caratteri font-safe (previene glifi mancanti o quadrati a schermo). |
| **`gust_tools/`** | Eseguibili ufficiali Gust per unpack e repack degli archivi PAK. |

---

## Installazione Manuale (Alternativa)

Se preferisci eseguire i comandi singolarmente da terminale:
```bash
# 1. Estrai PACK00.pak
cd pak_work && ..\gust_tools\gust_pak.exe "<CartellaGioco>\Data\PACK00.pak" && cd ..

# 2. Inietta la traduzione italiana
python src/yumia_text_tool.py apply spa pak_work\master project_yumia_es_en.json

# 3. Ricompila e copia nel gioco
cd pak_work && ..\gust_tools\gust_pak.exe PACK00.json && cd ..
copy /y pak_work\PACK00.pak "<CartellaGioco>\Data\PACK00.pak"
```

---

## Note sui Glifi e Font
I font originali dello slot spagnolo nel motore Gust non includono le vocali con accento grave (`à`, `è`, `ì`, `ò`, `ù`), che verrebbero renderizzate nel gioco come quadrati vuoti (*tofu*). Lo script `fix_accents.py` converte automaticamente le vocali accentate in formato sicuro (`a'`, `e'`, `i'`, `o'`, `u'`), garantendo una visualizzazione leggibile e senza glitch.

---

## Disclaimer

Progetto amatoriale di traduzione realizzato da fan, senza scopo di lucro e non affiliato con KOEI TECMO o GUST.  
*Atelier Yumia: The Alchemist of Memories & the Envisioned Land* è un marchio registrato e copyright di **KOEI TECMO GAMES CO., LTD.** / **GUST**.  
Questa patch richiede il possesso legittimo di una copia originale del gioco su Steam.
