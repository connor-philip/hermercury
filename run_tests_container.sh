#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo $DIR

if [[ $1 == "build" ]]; then
    docker build -t vmc_tests $DIR
fi

docker run -l hermercury_tests_container -v $DIR:/app vmc_tests


if [[ $? == 0 ]]; then
    echo "Deleting container:"
    docker rm `docker ps -qaf label=hermercury_tests_container`
fi