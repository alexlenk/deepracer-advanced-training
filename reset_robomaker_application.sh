#!/bin/sh

app_arn=$(aws robomaker list-simulation-applications --region=us-east-1 | grep -o arn:.*deepracer-simapp-[^\"]*)
aws robomaker update-simulation-application --sources="s3Bucket=deepracer-managed-resources-us-east-1,s3Key=deepracer-simapp.tar.gz,architecture=X86_64" --application="$app_arn" --simulation-software-suite="name=Gazebo,version=7" --robot-software-suite="name=ROS,version=Kinetic" --rendering-engine="name=OGRE,version=1.x" --region=us-east-1