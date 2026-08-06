# Neustart mit funktionierendem Netzwerk

Diese Umgebung blockte `openrouter.ai` (Embeddings) und `openaipublic.blob.core.windows.net`
(tiktoken) per Netzwerk-Policy. Ohne diese Hosts läuft das RAG-System nicht. So richtest du eine
Umgebung ein, in der es läuft, und startest sauber neu.

## 1. Netzwerk-Policy setzen (einmalig, in der Web-App)

Auf **claude.ai/code**:

1. Über dem Nachrichtenfeld auf das **Cloud-Icon** (Umgebungs-Auswahl) klicken.
2. **Add cloud environment** wählen, oder bei einer bestehenden Umgebung auf das **Zahnrad** (erscheint beim Hover).
3. Im Dialog **Network access** auf **Custom** stellen.
4. Im Feld **Allowed domains** je Zeile eintragen:
   ```
   openrouter.ai
   openaipublic.blob.core.windows.net
   ```
5. Häkchen bei **„Also include default list of common package managers"** setzen (damit `uv`/pip weiter funktioniert).
6. **Create/Save environment**.

Einfacher, aber offener: **Network access = Full** (jede Domain). Reicht ebenfalls.

Hinweis: Den **API-Key NICHT** in die Environment-Variablen des Dialogs schreiben — die sind für alle
Nutzer der Umgebung sichtbar und kein Secret-Store. Key stattdessen in der Session per Chat geben,
Claude schreibt ihn in die (ge-gitignorete) `.env`.

## 2. Neue Session auf diesem Branch starten

Neue Cloud-Session mit dieser Umgebung, Repo `Anna-neuu`, Branch **`claude/new-session-ww3cr2`**.
Falls die Session auf dem Default-Branch startet: Claude bitten, auf diesen Branch zu wechseln.

## 3. Korpus-PDFs bereitstellen

Die Quell-PDFs sind urheberrechtlich geschützt und liegen **nicht im Git**. Zwei Wege:

- **Falls im Git committet** (siehe Frage an die Verfasserin): nichts zu tun, sie sind schon da.
- **Sonst:** die `Anna.zip` erneut hochladen und Claude sagen: „rekonstruiere den Korpus".
  Claude führt aus:
  ```bash
  bash tools/rebuild-anna-corpus.sh /pfad/zur/hochgeladenen/Anna.zip
  ```

## 4. Key setzen und indexieren

```bash
# .env mit dem OpenRouter-Key (Claude erledigt das nach Key-Eingabe im Chat)
uv run python -m rag index --thesis anna-postmigrantisch-theater
uv run python -m rag corpus --thesis anna-postmigrantisch-theater --pretty   # Print-Offsets prüfen
uv run python -m rag bib   --thesis anna-postmigrantisch-theater --build --pretty
```

Danach: `bachelorarbeit-arbeitsweise` aktiv halten und Kapitel für Kapitel nach dem
Sieben-Schritt-Ritual belegen. Vollständiger Kontext in dieser Ordner-`CLAUDE.md`.

## Sanity-Check der Erreichbarkeit

```bash
curl -sS -o /dev/null -w "openrouter: %{http_code}\n"  --max-time 15 https://openrouter.ai/api/v1/models
curl -sS -o /dev/null -w "tiktoken:  %{http_code}\n"  --max-time 15 https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken
```
Beide sollten nicht `000`/403 sein.
