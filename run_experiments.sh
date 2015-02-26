#!/bin/bash

STRATEGY=1
NUMS=500000
POOLSIZE=4

time python factors.py $STRATEGY $NUMS $POOLSIZE
