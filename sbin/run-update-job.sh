#!/usr/bin/env bash

set -xe

function run(){
    DIR=$(dirname $0)
    BASEDIR=${DIR}/..

    export PYTHONPATH=
    run-data-pull-jhu.sh

}

run "$@"