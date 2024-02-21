#!/bin/bash

export CONTAINER_NAME=$2

if [ "$1" = "build" ]; then
  sudo docker-compose build
elif [ "$1" = "start" ]; then
  sudo docker-compose up -d
elif [ "$1" = "stop" ]; then
  if [ -z "$2" ]; then
    echo "Uso: sudo bash run.sh stop {parametro}"
  else
    sudo docker stop cems_container_$2
  fi
elif [ "$1" = "down" ]; then
  sudo docker-compose down
else
  echo "Comando no reconocido."
fi
