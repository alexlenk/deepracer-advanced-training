#!/bin/bash

aws s3 cp s3://deepracer-managed-resources-us-east-1/deepracer-simapp.tar.gz .
curl https://raw.githubusercontent.com/aws-samples/aws-deepracer-workshops/master/Advanced%20workshops/AI%20Driving%20Olympics%202019/challenge_train_w_PPO/sim_app_bundler.py -o sim_app_bundler.py
python3 sim_app_bundler.py --untar deepracer-simapp.tar.gz
DIR="build/simapp/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment"
mv $DIR/meshes $DIR/meshes.org
ln -s ./meshes.org $DIR/meshes