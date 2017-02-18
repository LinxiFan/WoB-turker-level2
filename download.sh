#!/bin/bash
function get() {
    wget http://ec2-52-33-170-48.us-west-2.compute.amazonaws.com:8080/$1 -O $1
    if [[ $# -eq 2 ]]; then
        less $1
    fi
}

get data/level2.jsonl -v
get data/progress.json

# ssh -i wob_openai.pem ubuntu@ec2-52-33-170-48.us-west-2.compute.amazonaws.com
