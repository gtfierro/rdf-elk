#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Usage: python make223p.py <path to model ttl file>'
    exit 0
fi

if [ -d node_modules/elkjs-svg ]
then
    cp ./elkjs-svg.js node_modules/elkjs-svg/elkjs-svg.js
else
    npm install
    cp ./elkjs-svg.js node_modules/elkjs-svg/elkjs-svg.js
fi


poetry run python make223p.py $1 | tee output.js
node output.js > $(basename $1).svg
