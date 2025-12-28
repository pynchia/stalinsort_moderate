#!/usr/bin/env bash
python sort.py <(shuf -i 0-1000 -n $1)
