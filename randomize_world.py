import random
import time
import os
from os import path
import subprocess
import sys

print("CLI Args:")
print(sys.argv)

restart_time = 3600

if os.environ["S3_YAML_NAME"].split("_")[0] == "eval":
    os.environ["JOB_TYPE"] = "EVALUATION"
else:
    os.environ["JOB_TYPE"] = "TRAINING"

p = subprocess.Popen("export", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
print(output)

if not path.isfile('/home/robomaker/randomize_world.sh') and os.environ["JOB_TYPE"] == "TRAINING":
    print("################## Executing randomize_world.sh ##################")
    WORLDS=["New_York_Track", "China_track", "Virtual_May19_Train_track", "Mexico_track", "Tokyo_Training_track", "Canada_Training", "Bowtie_track"]
    os.environ["WORLD_NAME"] = random.choice(WORLDS)
    print("Downloading script ...")
    p = subprocess.Popen("curl https://raw.githubusercontent.com/alexlenk/deepracer-advanced-training/master/randomize_world.sh -o /home/robomaker/randomize_world.sh \n /bin/bash /home/robomaker/randomize_world.sh " + os.environ["WORLD_NAME"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    print(output)
    if err is not None:
        print("################### ERROR: " + str(err))

    print("Scheduling restart in " + str(restart_time) + " seconds ...")
    subprocess.Popen("sleep " + str(restart_time) + ";aws robomaker restart-simulation-job --job=\"$AWS_ROBOMAKER_SIMULATION_JOB_ARN\" --region=us-east-1", shell=True)
    print("Script done...")
else:
    print("Skipping World Randomization in " + os.environ["JOB_TYPE"] + " Job")

print("World: " + os.environ["WORLD_NAME"])