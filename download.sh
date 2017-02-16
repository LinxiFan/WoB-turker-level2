#!/bin/bash
wget http://ec2-52-33-170-48.us-west-2.compute.amazonaws.com:8080/data.jsonl -O turker.jsonl
less turker.jsonl

# ssh -i wob_openai.pem ubuntu@ec2-52-33-170-48.us-west-2.compute.amazonaws.com
