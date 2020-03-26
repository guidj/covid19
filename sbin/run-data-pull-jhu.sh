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
    head -n 10 $BASEDIR/data/jhu/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv

}

run "$@"