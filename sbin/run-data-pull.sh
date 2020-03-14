#!/usr/bin/env bash

set -xe

function run(){
    DIR=$(dirname $0)
    BASEDIR=${DIR}/../

    export PYTHONPATH="$BASEDIR/py:$PYTHONPATH"
    scrapy runspider py/covid19/data/fetch.py "$@"
}

run "$@"