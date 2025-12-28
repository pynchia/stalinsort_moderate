#!/usr/bin/env bash
python sort.py <(shuf -i 0-10000 -n $1)
