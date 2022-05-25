#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Usage: python makeBrick.py <path to model ttl file>'
    exit 0
fi

poetry run python makeBrick.py $1
cat output.js
node output.js > $(basename $1).svg
