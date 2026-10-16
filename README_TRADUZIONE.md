# Traduzione Italiana - Atelier Yumia (pipeline ES->IT)
# Cartella di lavoro: C:\Users\David\Documents\yumia_ita

## Stato: pipeline verificato end-to-end
- Estrazione pak: OK (gust_pak v1.58, formato A22/A26)
- Parser EBM Yumia: OK, roundtrip byte-perfect su 767/767 file
- Progetto estratto: 27.701 segmenti (106.217 parole dialoghi + 182.390 parole UI)
- Ripack pak: OK

## File
- yumia_text_tool.py  -> estrazione/applicazione testi (EBM A26 + message.json)
- yumia_translate.py  -> traduzione AI multi-thread (endpoint compatibile OpenAI)
- project_yumia_es_en.json -> progetto: sorgente spagnolo + riferimento inglese ("dst" vuoto = da tradurre)
- pak_work\           -> pak estratto: master\spa\, master\eng\, PACK00.json
- gust_tools\         -> gust_pak.exe (estrazione/ricompilazione pak)
- glossary.json (da creare) -> opzionale ma consigliato

## Tradurre (lancia da C:\Users\David\Documents\yumia_ita)
1. (Consigliato) crea glossary.json: {"termina ES o EN": "termine italiano", ...}
2. Con Ollama locale:
   python yumia_translate.py project_yumia_es_en.json ^
     --endpoint http://localhost:11434/v1 --model qwen2.5:7b-instruct ^
     --workers 8 --glossary glossary.json
   Con API cloud:
   python yumia_translate.py project_yumia_es_en.json ^
     --endpoint https://api.openai.com/v1 --model gpt-4o-mini ^
     --api-key SK-... --workers 12 --glossary glossary.json
   - Riavviabile: rilancia lo stesso comando per completare i buchi.
   - Con GPU media locale: 2-5 ore. Con API veloce: 15-45 minuti.

## Applicare e ricostruire
1. python yumia_text_tool.py apply spa pak_work\master project_yumia_es_en.json
   (sovrascrive i file in pak_work\master\spa\ con le traduzioni in "dst")
2. cd pak_work ; ..\gust_tools\gust_pak.exe PACK00.json   (ricrea PACK00.pak)
3. BACKUP: rinomina <gioco>\Data\PACK00.pak in PACK00.pak.original
4. Copia pak_work\PACK00.pak in <gioco>\Data\
5. Nel gioco imposta la lingua SPAGNOLO: vedrai l'italiano.
   Nota: la verifica integrità di Steam ripristinerà il pak originale (rifai il punto 4).

## Aggiornamenti del gioco
Se un patch cambia i testi: ri-estrai il nuovo PACK00.pak, ri-genera il progetto
(extract) e ri-traduci: i segmenti identici agli originali si riallineano da soli
solo se il glossario è usato; altrimenti valuta di ri-tradurre solo le differenze.

