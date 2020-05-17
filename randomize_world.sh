#!/bin/sh

WORLD=$1
echo Copying Folder ...
cp -rf /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes.org /home/robomaker/meshes
ls -al /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes/
echo Modifying World: $WORLD ...

GRASS_TEXTURES_SIMPLE=(New_York_Track/textures/Wood.png reinvent/textures/Road_DIFF.png New_York_Track/textures/Concrete_01.png New_York_Track/textures/Concrete_02.png New_York_Track/textures/Concrete_03.png New_York_Track/textures/Concrete_04.png New_York_Track/textures/Concrete_05.png New_York_Track/textures/Concrete_06.png New_York_Track/textures/Concrete_07.png Canada_Training/textures/Canada_track_concrete_T_01.png Canada_Training/textures/Canada_track_concrete_T_02.png Canada_Training/textures/Canada_track_concrete_T_03.png Canada_Training/textures/Canada_track_concrete_T_04.png Canada_Training/textures/Canada_track_concrete_T_05.png New_York_Track/textures/Track_road_01.png)
GRASS_TEXTURES=(China_track/textures/China_track_landmark_U_01.png China_track/textures/China_track_landmark_U_04.png China_track/textures/China_track_landmark_U_07.png China_track/textures/China_track_glass_T_01.png China_track/textures/China_track_glass_T_03.png China_track/textures/China_track_glass_T_05.png China_track/textures/China_track_sea_U_02.png China_track/textures/China_track_sign_U_01.png Mexico_track/textures/Mexico_track_door_U_02.png Mexico_track/textures/Mexico_track_door_U_01.png Mexico_track/textures/Mexico_track_landmark_U_02.png Mexico_track/textures/Mexico_track_landmark_U_03_01.png Mexico_track/textures/Mexico_track_landmark_U_03_02.png Mexico_track/textures/Mexico_track_landmark_U_05.png Mexico_track/textures/Mexico_track_building_wall_U_01.png Canada_Training/textures/Canada_track_cloud_T_01.png Canada_Training/textures/Canada_track_building_wall_U_01.png New_York_Track/textures/Signs_02.png)

ROAD_TEXTURES_SIMPLE=(reInvent2019_track/textures/Bowtie_track_field.png reinvent/textures/Grass_DIFF.pngNew_York_Track/textures/Concrete_01.png New_York_Track/textures/Concrete_02.png New_York_Track/textures/Concrete_03.png New_York_Track/textures/Concrete_04.png New_York_Track/textures/Concrete_05.png New_York_Track/textures/Concrete_06.png New_York_Track/textures/Concrete_07.png Canada_Training/textures/Canada_track_concrete_T_01.png Canada_Training/textures/Canada_track_concrete_T_02.png Canada_Training/textures/Canada_track_concrete_T_03.png Canada_Training/textures/Canada_track_concrete_T_04.png Canada_Training/textures/Canada_track_concrete_T_05.png New_York_Track/textures/Wood.png Virtual_May19_Train_track/textures/Virtual_May19_Comp_track_field.png New_York_Track/textures/Track_field_grass_01.png reInvent2019_track/textures/Bowtie_track_field.png reinvent/textures/Grass_DIFF.png)
ROAD_TEXTURES=(China_track/textures/China_track_landmark_U_01.png China_track/textures/China_track_landmark_U_04.png China_track/textures/China_track_landmark_U_07.png China_track/textures/China_track_glass_T_01.png China_track/textures/China_track_glass_T_03.png China_track/textures/China_track_glass_T_05.png China_track/textures/China_track_sea_U_02.png China_track/textures/China_track_sign_U_01.png Mexico_track/textures/Mexico_track_door_U_02.png Mexico_track/textures/Mexico_track_door_U_01.png Mexico_track/textures/Mexico_track_landmark_U_02.png Mexico_track/textures/Mexico_track_landmark_U_03_01.png Mexico_track/textures/Mexico_track_landmark_U_03_02.png Mexico_track/textures/Mexico_track_landmark_U_05.png Mexico_track/textures/Mexico_track_building_wall_U_01.png Canada_Training/textures/Canada_track_cloud_T_01.png Canada_Training/textures/Canada_track_building_wall_U_01.png New_York_Track/textures/Signs_02.png) 

WALL_TEXTURES=(reinvent/textures/walls_light.jpg reinvent/textures/walls_org.jpg reinvent/textures/walls_dark.jpg)
WALL_TEXTURES2019=(reInvent2019_track/textures/walls_light.png reInvent2019_track/textures/wall.png reInvent2019_track/textures/walls_dark.png)

declare -A GRASS
GRASS[New_York_Track]=New_York_Track/textures/Track_field_grass_01.png
GRASS[China_track]=China_track/textures/China_track_field_grass_T_01.png
GRASS[Virtual_May19_Train_track]=Virtual_May19_Train_track/textures/Virtual_May19_Comp_track_field.png
GRASS[Mexico_track]=Mexico_track/textures/Mexico_Track_field_grass_T_01.png
GRASS[Tokyo_Training_track]=Tokyo_Training_track/textures/Track_field_grass_01.png
GRASS[reInvent2019_track]=reInvent2019_track/textures/Bowtie_track_field.png
GRASS[reinvent_base]=reinvent/textures/Grass_DIFF.png
GRASS[Canada_Training]=Canada_Training/textures/Canada_track_field_grass_01.png
GRASS[Bowtie_track]=Bowtie_track/textures/Bowtie_track_field.png
GRASS[Spain_track]=Spain_track/textures/Spain_Track_field_grass_T_01.png

declare -A ROADS
ROADS[New_York_Track]=New_York_Track/textures/Track_road_01.png
ROADS[China_track]=China_track/textures/China_track_road_T_01.png
ROADS[Virtual_May19_Train_track]=Virtual_May19_Train_track/textures/Virtual_May19_Comp_track_road.png
ROADS[Mexico_track]=Mexico_track/textures/Mexico_track_road_T_01.png
ROADS[Tokyo_Training_track]=Tokyo_Training_track/textures/Track_road_01.png
ROADS[reInvent2019_track]=reInvent2019_track/textures/Bowtie_track_road.png
ROADS[reinvent_base]=reinvent/textures/Road_DIFF.png
ROADS[Canada_Training]=Canada_Training/textures/Canada_track_road_T_01.png
ROADS[Bowtie_track]=Bowtie_track/textures/Bowtie_track_road.png
ROADS[Spain_track]=Spain_track/textures/Spain_track_road_T_01.png

declare -A WALLS
WALLS[reInvent2019_track]=reInvent2019_track/textures/wall.png
WALLS[reinvent_base]=reinvent/textures/walls.jpg

#cp /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes.org/China_track/textures/China_track_landmark_U_07.png /home/robomaker/meshes/Spain_track/textures/Spain_Track_field_grass_T_01.png 
TEX_ROAD=${ROAD_TEXTURES[$RANDOM % ${#ROAD_TEXTURES[@]} ]}
TEX_GRASS=${GRASS_TEXTURES[$RANDOM % ${#GRASS_TEXTURES[@]} ]}

echo Grass: Replacing ${GRASS[$WORLD]} with $TEX_GRASS
echo Road: Replacing ${ROADS[$WORLD]} with $TEX_ROAD

cp /home/robomaker/meshes/$TEX_ROAD /home/robomaker/meshes/${ROADS[$WORLD]}
cp /home/robomaker/meshes/$TEX_GRASS /home/robomaker/meshes/${GRASS[$WORLD]}

echo Done!