#!/bin/bash

aws s3 cp s3://deepracer-managed-resources-us-east-1/deepracer-simapp.tar.gz .
curl https://raw.githubusercontent.com/aws-samples/aws-deepracer-workshops/master/Advanced%20workshops/AI%20Driving%20Olympics%202019/challenge_train_w_PPO/sim_app_bundler.py -o sim_app_bundler.py
python3 sim_app_bundler.py --untar deepracer-simapp.tar.gz
DIR="build/simapp/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment"
mv $DIR/meshes $DIR/meshes.org
ln -s /home/robomaker/meshes $DIR/meshes

sed -i 's/rospy.get_param("WORLD_NAME")/os.environ["WORLD_NAME"]/g' build/simapp/bundle/opt/install/sagemaker_rl_agent/lib/python3.5/site-packages/markov/track_geom/track_data.py
sed -i 's/rospy.get_param("WORLD_NAME")/os.environ["WORLD_NAME"]/g' build/simapp/bundle/opt/install/deepracer_simulation_environment/lib/python2.7/dist-packages/mp4_saving/utils.py

sed -i 's/import roslaunch/import subprocess, sys\
subprocess.call("curl https:\/\/raw.githubusercontent.com\/alexlenk\/deepracer-advanced-training\/master\/randomize_world.py -o \/home\/robomaker\/randomize_world.py", shell=True)\
sys.path.insert(1, "\/home\/robomaker")\
import randomize_world\
import roslaunch/g' build/simapp/bundle/opt/ros/kinetic/bin/roslaunch
python3 sim_app_bundler.py --tar

s3_bucket=$(aws s3 ls --region=us-east-1 | grep -o deepracer-simapp-.*)
if [ "$s3_bucket" = "" ]; then
    s3_bucket=deepracer-simapp-$(uuidgen)
fi
aws s3 mb s3://$s3_bucket --region=us-east-1
aws s3 cp build/output.tar.gz s3://$s3_bucket/deepracer-custom-simapp.tar.gz --region=us-east-1
app_arn=$(aws robomaker list-simulation-applications --region=us-east-1 | grep -o arn:.*deepracer-simapp-[^\"]*)
aws robomaker update-simulation-application --sources="s3Bucket=$s3_bucket,s3Key=deepracer-custom-simapp.tar.gz,architecture=X86_64" --application="$app_arn" --simulation-software-suite="name=Gazebo,version=7" --robot-software-suite="name=ROS,version=Kinetic" --rendering-engine="name=OGRE,version=1.x" --region=us-east-1
