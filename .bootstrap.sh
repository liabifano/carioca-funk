#!/usr/bin/env bash

set -eo pipefail

DEFAULT_JOB='skeleton'
FILES="Dockerfile Makefile setup.py"
FOLDERS="src/${DEFAULT_JOB}/"



while getopts ":j:" opt; do
  case $opt in
      j) JOB_NAME="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done



function check-inputs () {

    if [[ -z "$JOB_NAME" ]]; then
        echo "You must specify the job name with the flag -j"
        exit 1
    fi

}


function rename-inside () {

    for f in $FILES
    do
        sed -i.bak "s/${DEFAULT_JOB}/${JOB_NAME}/" $f
        rm -- "${f}.bak"
    done;

}


function remove-secrets () {

    sed -i.bak "/env:/d" .travis.yml && sed -i.bak "/global/d" .travis.yml && sed -i.bak "/- secure/d" .travis.yml
    rm -- ".travis.yml.bak" || true

}


function get-secrets () {

    travis login --pro --auto

    if [ -z "$DOCKER_USERNAME" ]
    then
        echo "Please, enter your dockerhub login"
        echo
        read DOCKER_USERNAME
    fi

    travis encrypt --com DOCKER_USERNAME=$DOCKER_USERNAME --add

    if [ -z "$DOCKER_PASSWORD" ]
    then
        echo "Please, enter you dockerhub password - no one want to steal it"
        echo
        read DOCKER_PASSWORD
    fi

    travis encrypt --com DOCKER_PASSWORD=$DOCKER_PASSWORD --add

}


function undo-rename-inside() {

    for f in $FILES
    do
        sed -i.bak "s/${JOB_NAME}/${DEFAULT_JOB}/" $f
        rm -- "${f}.bak"
    done;

}


function rename-folders () {

    for f in $FOLDERS
    do
        NEWFOLDER=${f//${DEFAULT_JOB}/${JOB_NAME}}
        mv $f ${NEWFOLDER}
    done;

}

function undo-rename-folders() {
    FOLDERS="src/${DEFAULT_JOB}/"

    for f in $FOLDERS
    do
        OLDFOLDER=${f//${DEFAULT_JOB}/${JOB_NAME}}
        NEWFOLDER=${f//${JOB_NAME}/"${DEFAULT_JOB}"}
        mv ${OLDFOLDER} ${NEWFOLDER}
    done;
}



function up () {

    (check-inputs)
    (rename-inside)
    (rename-folders)

}

function generate-travis-secrets () {

    (remove-secrets)
    (get-secrets)

}


function down () {

    (check-inputs)
    (undo-rename-inside)
    (undo-rename-folders)
    (remove-secrets)

}


case "${@: -1}" in
  (up)
    up
    exit 0
    ;;
  (down)
      down
    exit 0
    ;;
  (travis)
      generate-travis-secrets
    exit 0
    ;;
  (*)
    echo "Usage: $0 { up | down }"
    exit 2
    ;;
esac
