#!/usr/bin/env bash

set -xe

function run(){
    DIR=$(dirname $0)
    BASEDIR=${DIR}/..

    export PYTHONPATH=$BASEDIR/py
    sh $BASEDIR/sbin/run-data-pull-jhu.sh
    python -m covid19.data.preproc \
      --input-path=/Users/guilherme/code/covid19/data/jhu/csse_covid_19_data/csse_covid_19_daily_reports/ \
      --output-path=/Users/guilherme/code/covid19/data/jhu/processed
    python -m covid19.viz.partials \
      --plots-path=/Users/guilherme/code/covid19/data/jhu/processed/charts \
      --output-path=/Users/guilherme/code/covid19/docs/_partials \
      --files region-agg-chart.html world-agg-chart.html

}

run "$@"