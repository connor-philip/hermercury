#!/usr/bin/env bash

PROJECTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )
echo $PROJECTDIR

if [[ $1 == "build" ]]; then
    docker build --tag hermercury_tests $PROJECTDIR
fi

echo "Running unit tests..."
docker run --label hermercury_tests_container --volume $PROJECTDIR:/app hermercury_tests
echo "...done"
echo "Deleting container:"
docker rm `docker ps -qaf label=hermercury_tests_container`
