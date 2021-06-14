
        echo =====Sondensucher aktualisiert=====
   		cd ./sondensucher/
        git pull
        cd /

python3 ./sondensucher/Python/config.py &

sleep 15



python3 ./sondensucher/Python/mqtt.py &
python3 ./sondensucher/Python/API.py &
python3 ./sondensucher/Python/loop.py
