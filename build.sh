#!/bin/bash
docker network create flask;
docker volume create sqlite;
docker-compose up -d 
