#!/bin/bash
docker network create flask;
docker volume create postgres;
docker-compose up -d 
