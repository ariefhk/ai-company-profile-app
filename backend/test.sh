#!/bin/bash

if [ -n "$1" ]; then
    pytest "tests/$1" -v
else
    pytest tests/ -v
fi
