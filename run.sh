#!/bin/bash

PY=$(which pypy)

if [[ -z $PY ]]; then
    PY=python
fi

$PY src
