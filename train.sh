#!/bin/bash



src="./src/training.py"
training="./data/icwb2-data/training/pku_training.utf8"
result="../pku_utf8.model"
time=100


time python $src $training $result $time