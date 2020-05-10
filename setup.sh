#!/bin/bash

aws s3 cp s3://neurips-aido3-awsdeepracer/build.tar.gz .
tar xvfz build.tar.gz
curl https://raw.githubusercontent.com/aws-samples/aws-deepracer-workshops/master/Advanced%20workshops/AI%20Driving%20Olympics%202019/challenge_train_w_PPO/sim_app_bundler.py -o sim_app_bundler.py
aws s3 cp s3://deepracer-managed-resources-us-east-1/deepracer-simapp.tar.gz .
mkdir deepracer-simapp
tar xvfz deepracer-simapp.tar.gz -C deepracer-simapp
rm -rf build/simapp/bundle/*
tar xvf deepracer-simapp/bundle.tar -C build/simapp/bundle