
        echo =====Sondensucher aktualisiert=====
   		cd ./sondensucher/
        git pull
        cd /

sleep 15
python3 ./sondensucher/Python/Database.py
python3 ./sondensucher/Python/mqtt.py &
#TODO API in loop Aufrufen
python3 ./sondensucher/Python/API.py &
python3 ./sondensucher/Python/loop.py

#TODO Überprüfung einfügen dass alle Skripte laufen