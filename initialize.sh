#!/bin/bash

if [[ $# -eq 0 ]] # Case for no arguments passed, run as is.
then
	rm -rf etc
    mkdir etc
    cp /etc/passwd etc/
    cp /etc/group etc/
    docker-compose build
    docker-compose up

elif [[ $# -ne 0 ]] # Case for more than one argument passed, either test or file specific.
then
    if [[ $1 == "test" ]]   # If passed in with test parameter, will run pytest tests.
    then
        rm -rf etc
        mkdir etc
        cp tests/passwd etc/
        cp tests/group etc/
        docker-compose build
        docker-compose run --rm --entrypoint "python -m pytest --rootdir=/usr/src/app --disable-warnings" password-service
    else                    # Otherwise, the parameter is the path to the folder containing the group/user info.
        rm -rf etc
        mkdir etc
        cp $1/passwd etc
        cp $1/group etc
        docker-compose build
        docker-compose up
    fi
fi