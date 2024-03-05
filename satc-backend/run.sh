#!/bin/bash

export CONTAINER_NAME=$2

if [ "$1" = "build" ]; then
  sudo docker-compose build
elif [ "$1" = "start" ]; then
  sudo docker-compose up -d
elif [ "$1" = "stop" ]; then
  sudo docker-compose stop
elif [ "$1" = "down" ]; then
  sudo docker-compose down
else
  echo "Comando no reconocido."
fi
