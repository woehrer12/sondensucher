# sondensucher

## Install

Ubuntu:
```bash
git clone https://github.com/woehrer12/skripte.git
skripte/sondensucher.sh
```

## API
Abruf für eine bestimmt Sonde mit:

http://127.0.0.1:5000/api/v1/resources/sonden?id={id}

Beispiel:

http://127.0.0.1:5000/api/v1/resources/sonden?id=P2830105

Abruf für alle aktiven Sonden:

http://127.0.0.1:5000/api/v1/resources/sonden/all


## Webinterface

http://127.0.0.1:5000

## Prediction

Ist einzusehen unter der direkten Seite zur Sonde. Prediction funktioniert nur wenn der Startort bekannt und angelegt ist.