#!/bin/sh

s3_bucket=$(aws s3 ls --region=us-east-1 | grep -o deepracer-simapp-.*)
app_arn=$(aws robomaker list-simulation-applications --region=us-east-1 | grep -o arn:.*deepracer-simapp-[^\"]*)
aws robomaker update-simulation-application --sources="s3Bucket=$s3_bucket,s3Key=deepracer-custom-simapp.tar.gz,architecture=X86_64" --application="$app_arn" --simulation-software-suite="name=Gazebo,version=7" --robot-software-suite="name=ROS,version=Kinetic" --rendering-engine="name=OGRE,version=1.x" --region=us-east-1
