#!/bin/bash

if [ ! -d "./ex1" ]
then
    mkdir ex1
    tar -C ex1 -xzf ex1-prod.tar.gz
    cd ex1
    docker load -i web-server.tar
    docker load -i sql-server.tar
else
    cd ex1
fi
docker-compose up -d
