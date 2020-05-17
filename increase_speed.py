#!/usr/bin/python

import json
import os
import time
import sys

base_s3 = "s3://" + os.popen('aws s3 ls | grep -o -E aws-deepracer-[0-9a-z-]*').read().strip()
print("S3 URL: " + base_s3)

def increase_speed(job, sleep = 45, percentage = 1.15, wait = True):
    sleep_now = sleep
    job_status = "starting"
    
    while not (job_status == "canceled" or job_status == "canceled"):
        if wait:
            os.system("date")
            print("Waiting for " + str(sleep_now) + " minutes ...")
            time.sleep(sleep_now*60)

        job_description = json.loads(os.popen('aws robomaker describe-simulation-job --job=' + job).read())
        model = job_description["simulationApplications"][0]["launchConfig"]["environmentVariables"]["MODEL_METADATA_FILE_S3_KEY"]
        model_s3 = base_s3 + "/" + model
        job_status = job_description["status"].lower()
        if job_status == "running":
            skip = update_model_metadata(model_s3, percentage)
            sleep_now = sleep
        else:
            print("Job not running ...")
            skip = True
            sleep_now = 5
        if not skip:
            print("Restarting job ...")
            os.system("aws robomaker restart-simulation-job --job=" + job)
        else:
            print("Skipping Restart.")
        wait = True


def update_model_metadata(model_s3, percentage):
    print("Increasing speed by " + str(int((percentage-1)*100)) + " % ...")
    os.system("aws s3 cp " + model_s3 + " ./model_metadata.json")
    with open("model_metadata.json") as infile:
        model_metadata = json.load(infile)
    speeds = set()
    speeds_new = set()
    for item in model_metadata["action_space"]:
        speeds.add(item["speed"])
        
    speeds = sorted(speeds)
    if max(speeds) == 4:
        skip = True
    else:
        skip = False
    for item in model_metadata["action_space"]:
        if item["speed"] == speeds[0]:
            item["speed"] = min(0.4, item["speed"]*percentage)
        elif len(speeds) == 3 and item["speed"] == speeds[1]:
            item["speed"] = min(1.0, item["speed"]*percentage)
        else:
            item["speed"] = min(3, item["speed"]*percentage)
        speeds_new.add(item["speed"])
        
    print("Old Speeds: " + str(speeds))
    print("New Speeds: " + str(sorted(speeds_new)))
    with open('model_metadata.json', 'w') as outfile:
        json.dump(model_metadata, outfile)
    os.system("aws s3 cp ./model_metadata.json " + model_s3) 
    return skip

if len(sys.argv) > 2:
    sleep = int(sys.argv[2])
else:
    sleep = 45
if len(sys.argv) > 3:
    percentage = float(sys.argv[3])
else:
    percentage = 1.15
if len(sys.argv) > 4:
    wait = sys.argv[4] == "True"
else:
    wait = True

increase_speed(sys.argv[1], sleep, percentage, wait)