from ubuntu
RUN command apt-get update
RUN command apt-get install sudo
#Git installieren
RUN command apt-get install git -y
#Skripte nachladen
RUN command git clone https://github.com/woehrer12/skripte.git
RUN command git clone https://github.com/woehrer12/sondensucher.git
#System Updaten
RUN command ./skripte/updater.sh
#Python installieren
RUN command apt install python3-pip -y
RUN command pip3 install mysql-connector-python

RUN echo HELLO

CMD [ "python3", "./sondensucher/Python/Database.py" ]