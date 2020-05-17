#!/bin/sh

export
echo Copying Folder ...
cp -rf /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes.org /home/robomaker/meshes
ls -al /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes/
echo Modifying Grass ...
cp /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes.org/China_track/textures/China_track_landmark_U_07.png /home/robomaker/meshes/Spain_track/textures/Spain_Track_field_grass_T_01.png 
ps aux
echo Done!