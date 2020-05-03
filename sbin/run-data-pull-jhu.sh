#!/usr/bin/env bash

set -xe

function run(){
    DIR=$(dirname $0)
    BASEDIR=${DIR}/..

    if [ -d $BASEDIR/data/jhu/.git ]; then
      cd $BASEDIR/data/jhu
      git pull
      cd ../../
    else
      git clone git@github.com:CSSEGISandData/COVID-19.git $BASEDIR/data/jhu
    fi;

}

run "$@"