docker build -t resultsuz_bot -f Dockerfile .

docker run -v /root/DataBase:/app/DataBase resultsuz_bot 
