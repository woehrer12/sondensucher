# sondensucher

## Install

Ubuntu:
```bash
git clone https://github.com/woehrer12/skripte.git
skripte/sondensucher.sh
```

## API
Abruf für eine bestimmt Sonde mit:

api.sondensucher.de:5000/api/v1/resources/sonden?id={id}

Beispiel:

api.sondensucher.de:5000/api/v1/resources/sonden?id=P2830105

Alle aktive Sonden mit Daten:

api.sondensucher.de:5000/api/v1/resources/sonden/all

Alle aktive Sonden mit Daten letzte 60 Minuten:

api.sondensucher.de:5000/api/v1/resources/sonden/all?min=60

Liste aller aktiven Sonden ohne Daten:

api.sondensucher.de:5000/api/v1/resources/sonden/list

Liste aller aktiven Sonden ohne Daten: letzte 60 Minuten

api.sondensucher.de:5000/api/v1/resources/sonden/list?min=60



## Webinterface

api.sondensucher.de:5000

## Prediction

Ist einzusehen unter der direkten Seite zur Sonde. Prediction funktioniert nur wenn der Startort bekannt und angelegt ist.