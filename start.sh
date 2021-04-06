
        echo =====Sondensucher aktualisiert=====
   		cd ./sondensucher/
        git pull
        cd /

sleep 15

python3 ./sondensucher/Python/API.py &
python3 ./sondensucher/Python/loop.py

#TODO Überprüfung einfügen dass alle Skripte laufen