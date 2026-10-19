# ASTRABRUCH – Downloads

Spielbare Testversionen für Linux, Windows, macOS und Android.

**[Zur Downloadseite](https://michalsy.github.io/astrabruch-downloads/)**

Dieses Repository enthält die Downloadseite und fertige Spielpakete in GitHub Releases. Der Spielcode bleibt privat. Veröffentlichung bedeutet keine Open-Source-Lizenz; enthaltene Drittanbieterhinweise stehen in den Paketen.

Die Seite wird bei jedem veröffentlichten Release einschließlich Vorabversionen automatisch neu erzeugt. Sie zeigt die höchste vollständige Version mit vier Plattformpaketen und Prüfsummen. Fehlende oder als Entwurf gespeicherte Releases erscheinen nicht.

Die Pakete sind Testversionen. macOS verwendet eine Ad-hoc-Signatur ohne Apple-Notarisierung; Windows hat derzeit kein Codesign-Zertifikat. Installationshinweise stehen auf der Downloadseite.

## Seite lokal prüfen

```sh
printf '[]' > /tmp/astrabruch-releases.json
python3 build-site.py --releases /tmp/astrabruch-releases.json --output dist
python3 -m http.server 8080 --directory dist
```
