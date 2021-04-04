sudo docker image rm sondensucher
sudo docker build -t sondensucher ./docker/sondensucher/
sudo docker image rm sondenweb
sudo docker build -t sondenweb ./docker/apache/