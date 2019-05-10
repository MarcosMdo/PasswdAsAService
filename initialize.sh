#!/bin/bash

if [[ $# -eq 0 ]] # Case for no arguments passed.
then
	cp /etc/passwd etc/
    cp /etc/group etc/
    docker-compose build
    docker-compose up

elif [[ $# -ne 0 ]] # Case for more than one argument passed
then
    rm -rf etc/*
    cp $1/passwd etc
    cp $1/group etc

    docker-compose build
    docker-compose up
fi