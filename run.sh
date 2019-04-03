#!/bin/bash



src="./src/wordtag.py"
training="./data/icwb2-data/training/pku_training.utf8"
testing="./data/icwb2-data/testing/pku_test.utf8"
result="pku_result.utf8"

python $src $training $testing $result