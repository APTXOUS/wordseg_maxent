#!/bin/bash



src="./src/testing.py"
model="../pku_utf8.model"
testing="./data/icwb2-data/testing/pku_test.utf8"
result="../pku_utf8.result"

time python $src $model $testing $result 