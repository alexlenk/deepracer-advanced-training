import random
import time
import os
from os import path
import subprocess
import sys
import yaml

if os.environ["S3_YAML_NAME"].split("_")[0] == "eval" or os.environ["JOB_TYPE"] == "EVALUATION":
    os.environ["JOB_TYPE"] = "EVALUATION"
else:
    os.environ["JOB_TYPE"] = "TRAINING"

p = subprocess.Popen("export", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
print(output)

if not path.isfile('/home/robomaker/randomize_world.sh') and os.environ["JOB_TYPE"] == "TRAINING":
    print("################## Executing randomize_world.sh ##################")
    print("Downloading script ...")
    WORLDS=["New_York_Track", "China_track", "Virtual_May19_Train_track", "Mexico_track", "Tokyo_Training_track", "Canada_Training", "Bowtie_track"]
    os.environ["WORLD_NAME"] = random.choice(WORLDS)
    p = subprocess.Popen("curl https://raw.githubusercontent.com/alexlenk/deepracer-advanced-training/master/randomize_world.sh -o /home/robomaker/randomize_world.sh \n /bin/bash /home/robomaker/randomize_world.sh " + os.environ["WORLD_NAME"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    print(output)
    if err is not None:
        print("################### ERROR: " + str(err))

    print("S3 Command: aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/jobtype -")
    p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/jobtype -", stdout=subprocess.PIPE, shell=True)
    (jobtype, err) = p.communicate()
    p_status = p.wait()

    jobtype = str(jobtype).strip()

    if jobtype == "EVALUATION":
        print("Switching Job Type to EVALUATION")
        os.environ["JOB_TYPE"] = "EVALUATION"
        p = subprocess.Popen("echo 'TRAINING' | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/jobtype", stdout=subprocess.PIPE, shell=True)
        os.environ["MODEL_S3_BUCKET"] = os.environ["SAGEMAKER_SHARED_S3_BUCKET"]
        os.environ["MODEL_S3_PREFIX"] = os.environ["SAGEMAKER_SHARED_S3_PREFIX"]
        restart_time = 600
        os.environ["WORLD_NAME"] = "reinvent_base"

        p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/" + os.environ["S3_YAML_NAME"] + " -", stdout=subprocess.PIPE, shell=True)
        (training_str, err) = p.communicate()
        p_status = p.wait()
        data = yaml.load(training_str)
        model_name = data["MODEL_METADATA_FILE_S3_KEY"].split("/")[1]
        eval_out = {
            "METRICS_S3_OBJECT_KEY": "DeepRacer-Metrics/EvaluationMetrics-Mideval.json",
            "AWS_REGION": data["AWS_REGION"],
            "MODEL_NAME": model_name,
            "NUMBER_OF_TRIALS": 20,
            "RACER_NAME": model_name,
            "CAR_NAME": model_name,
            "VIDEO_JOB_TYPE": "EVALUATION",
            "KINESIS_VIDEO_STREAM_NAME": data["KINESIS_VIDEO_STREAM_NAME"],
            "WORLD_NAME": "reinvent_base",
            "ROBOMAKER_SIMULATION_JOB_ACCOUNT_ID": int(data["ROBOMAKER_SIMULATION_JOB_ACCOUNT_ID"]),
            "DISPLAY_NAME": model_name,
            "SIMTRACE_S3_BUCKET": data["SIMTRACE_S3_BUCKET"],
            "METRICS_S3_BUCKET": data["METRICS_S3_BUCKET"],
            "SIMTRACE_S3_PREFIX": "DeepRacer-Logs/EvaluationLogs-Mideval",
            "MODEL_S3_PREFIX": data["SAGEMAKER_SHARED_S3_PREFIX"],
            "RACE_TYPE": data["RACE_TYPE"],
            "JOB_TYPE": "EVALUATION",
            "MODEL_S3_BUCKET": data["SAGEMAKER_SHARED_S3_BUCKET"],
            "CAR_COLOR": "Red"
        }
        print(yaml.dump(eval_out, explicit_start=True))
        os.environ["S3_YAML_NAME"] = "Mideval.yaml"
        p = subprocess.Popen("echo \"" + yaml.dump(eval_out, explicit_start=True) + "\" | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/" + os.environ["S3_YAML_NAME"], stdout=subprocess.PIPE, shell=True)
    else:
        print("Staying with Job Type to TRAINING")
        os.environ["JOB_TYPE"] = "TRAINING"
        p = subprocess.Popen("echo 'EVALUATION' | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/jobtype", stdout=subprocess.PIPE, shell=True)
        restart_time = 3600

    print("Scheduling restart in " + str(restart_time) + " seconds ...")
    subprocess.Popen("sleep " + str(restart_time) + ";aws robomaker restart-simulation-job --job=\"$AWS_ROBOMAKER_SIMULATION_JOB_ARN\" --region=us-east-1", shell=True)
    print("Script done...")
else:
    print("Skipping World Randomization in " + os.environ["JOB_TYPE"] + " Job")

if os.environ["JOB_TYPE"] == "EVALUATION" and not sys.argv[2] == "evaluation.launch":
    print("Setting launch type to: evaluation.launch")
    sys.argv[2] = "evaluation.launch"

print("World: " + os.environ["WORLD_NAME"])