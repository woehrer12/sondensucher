
        echo =====Sondensucher aktualisiert=====
   		cd ./sondensucher/
        git pull
        cd /

sleep 30
python3 ./sondensucher/Python/Database.py
python3 ./sondensucher/Python/mqtt.py &
python3 ./sondensucher/Python/loop.py