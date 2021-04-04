
        echo =====Sondensucher aktualisiert=====
   		cd ./sondensucher/
        git pull
        cd /

sleep 30
python3 ./sondensucher/Python/Database.py
python3 ./sondensucher/Python/mqtt.py & >/dev/null 2>&1
python3 ./sondensucher/Python/loop.py