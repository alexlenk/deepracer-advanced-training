import random
import time
import os
from os import path
import subprocess
import sys
import yaml
from datetime import datetime
import json

if not path.isdir('/home/robomaker/meshes'):
    print("Copying Folder ...")
    subprocess.call("cp -rf /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes.org /home/robomaker/meshes", shell=True)

def randomize():
    #p = subprocess.Popen("export", stdout=subprocess.PIPE, shell=True)
    #(output, err) = p.communicate()
    #p_status = p.wait()
    #print(output)
    #print(sys.argv)

    if os.environ["S3_YAML_NAME"].split("_")[0] == "eval" or os.environ.get("JOB_TYPE") == "EVALUATION":
        os.environ["JOB_TYPE"] = "EVALUATION"
    else:
        os.environ["JOB_TYPE"] = "TRAINING"
    eval_world = os.environ["WORLD_NAME"]
    if not path.isfile('/home/robomaker/randomize_world.sh') and os.environ["JOB_TYPE"] == "TRAINING":
        print("################## Executing randomize_world.sh ##################")
        print("Downloading script ...")
        WORLDS=["New_York_Track", "China_track", "Virtual_May19_Train_track", "Mexico_track", "Tokyo_Training_track", "Canada_Training", "Bowtie_track"]
        train_world = random.choice(WORLDS)
        os.environ["WORLD_NAME"] = train_world
        p = subprocess.Popen("curl https://raw.githubusercontent.com/alexlenk/deepracer-advanced-training/master/randomize_world.sh -o /home/robomaker/randomize_world.sh \n /bin/bash /home/robomaker/randomize_world.sh " + train_world, stdout=subprocess.PIPE, shell=True)
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
            os.environ["WORLD_NAME"] = eval_world

            p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/" + os.environ["S3_YAML_NAME"] + " -", stdout=subprocess.PIPE, shell=True)
            (training_str, err) = p.communicate()
            p_status = p.wait()
            data = yaml.load(training_str)
            model_name = data["MODEL_METADATA_FILE_S3_KEY"].split("/")[1]
            eval_out = {
                "METRICS_S3_OBJECT_KEY": os.environ["METRICS_S3_OBJECT_KEY"] + "-Mideval.json",
                "AWS_REGION": data["AWS_REGION"],
                "MODEL_NAME": model_name,
                "NUMBER_OF_TRIALS": 20000,
                "RACER_NAME": model_name,
                "CAR_NAME": model_name,
                "VIDEO_JOB_TYPE": "EVALUATION",
                "KINESIS_VIDEO_STREAM_NAME": data["KINESIS_VIDEO_STREAM_NAME"],
                "WORLD_NAME": os.environ["WORLD_NAME"],
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
            result = "---\n"
            for key, value in eval_out.items():
                result += key + ": \"" + str(value) +"\"\n"
            os.environ["S3_YAML_NAME"] = "Mideval.yaml"
            subprocess.call("echo '" + result + "' | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/" + os.environ["S3_YAML_NAME"], shell=True)
            p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["METRICS_S3_OBJECT_KEY"] + "-Mideval_Best.json -", stdout=subprocess.PIPE, shell=True)
            (best_eval, err) = p.communicate()
            p_status = p.wait()
            if best_eval.strip() != "":
                best_eval_metric = json.loads(best_eval)
                best_completion_percentage = [metric["completion_percentage"] for metric in best_eval_metric["metrics"]]
                best_elapsed_time_in_milliseconds = [metric["elapsed_time_in_milliseconds"] for metric in best_eval_metric["metrics"]]
                best_average = int(sum(best_completion_percentage)/len(best_completion_percentage))
                mean_round_time = int((sum(best_elapsed_time_in_milliseconds)/len(best_elapsed_time_in_milliseconds))/1000)
                restart_time = min(max(restart_time, int(mean_round_time/best_average) * 15), 25*60)
        else:
            print("Staying with Job Type to TRAINING")
            os.environ["JOB_TYPE"] = "TRAINING"
            subprocess.call("echo 'EVALUATION' | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/jobtype", shell=True)
            restart_time = 2700

            p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/" + os.environ["S3_YAML_NAME"] + " -", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            output = output.strip().replace(eval_world, os.environ["WORLD_NAME"])
            subprocess.call("echo '" + output + "' | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/" + os.environ["S3_YAML_NAME"], shell=True)

            p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["METRICS_S3_OBJECT_KEY"] + "-Mideval.json -", stdout=subprocess.PIPE, shell=True)
            (curr_eval, err) = p.communicate()
            p_status = p.wait()
            curr_full_rounds = 0
            curr_average = 0
            if curr_eval.strip() != "":
                curr_eval_metric = json.loads(curr_eval)
                curr_completion_percentage = [metric["completion_percentage"] for metric in curr_eval_metric["metrics"]]
                curr_full_rounds = len([i for i in curr_completion_percentage if i == 100])
                curr_average = sum(curr_completion_percentage)/len(curr_completion_percentage)
                print("Current Model: " + str(curr_completion_percentage))
                print("Current Full Rounds: " + str(curr_full_rounds)) + "/" + str(len(curr_completion_percentage)) + " (" + str(int(100*curr_full_rounds/len(curr_completion_percentage))) + "%)"
                print("Current Average Rounds: " + str(int(curr_average)))

            p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["METRICS_S3_OBJECT_KEY"] + "-Mideval_Best.json -", stdout=subprocess.PIPE, shell=True)
            (best_eval, err) = p.communicate()
            p_status = p.wait()
            best_full_rounds = 0
            best_average = 0
            if best_eval.strip() != "":
                best_eval_metric = json.loads(best_eval)
                best_completion_percentage = [metric["completion_percentage"] for metric in best_eval_metric["metrics"]]
                best_full_rounds = len([i for i in best_completion_percentage if i == 100])
                best_average = sum(best_completion_percentage)/len(best_completion_percentage)
                print("Best Model: " + str(best_completion_percentage))
                print("Best Full Rounds: " + str(best_full_rounds)) + "/" + str(len(best_completion_percentage)) + " (" + str(int(100*best_full_rounds/len(best_completion_percentage))) + "%)"
                print("Best Average Rounds: " + str(int(best_average)))

            #p = subprocess.Popen("aws s3 ls s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model_best", stdout=subprocess.PIPE, shell=True)
            #(data, err) = p.communicate()
            #p_status = p.wait()
            #model_best_not_exists = data.strip() == ""

            if curr_full_rounds > best_full_rounds or curr_full_rounds == best_full_rounds and curr_average >= best_average:
                subprocess.call("aws s3 cp s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["METRICS_S3_OBJECT_KEY"] + "-Mideval.json s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["METRICS_S3_OBJECT_KEY"] + "-Mideval_Best.json", shell=True)
                subprocess.call("aws s3 rm s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model_best/ --recursive", shell=True)
                #print("aws s3 sync s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model/ s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model_best/")
                subprocess.call("aws s3 sync s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model/ s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model_best/", shell=True)
                if curr_full_rounds > 0 or curr_average > 0:
                    print("New Best Model Found!!")
                    p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/trained_tracks -", stdout=subprocess.PIPE, shell=True)
                    (trained_tracks, err) = p.communicate()
                    p_status = p.wait()
                    trained_tracks = trained_tracks.strip()
                    if trained_tracks == "":
                        trained_tracks = "Date and Time\tFull Rounds\tFull Round %\tAverage Completed\n"
                    else:
                        trained_tracks += "\n"

                    trained_tracks += datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\t" + str(curr_full_rounds) + "/" + str(len(curr_completion_percentage)) + "\t" + str(int(100*curr_full_rounds/len(curr_completion_percentage))) + "%\t" + str(int(curr_average)) + "%"
                    subprocess.call("echo \"" + trained_tracks + "\" | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/trained_tracks --content-type=text/plain", shell=True)
            else:
                print("Restoring Old Model ...")
                subprocess.call("aws s3 rm s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model/ --recursive", shell=True)
                subprocess.call("aws s3 sync s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model_best/ s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/model/", shell=True)
                p = subprocess.Popen("aws s3 cp --quiet s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/failed_tracks -", stdout=subprocess.PIPE, shell=True)
                (failed_tracks, err) = p.communicate()
                p_status = p.wait()
                failed_tracks = failed_tracks.strip()

                if failed_tracks == "":
                    failed_tracks = "Date and Time\tFull Rounds\tFull Round %\tAverage Completed\n"
                else:
                    failed_tracks += "\n"
                failed_tracks += datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\t" + str(curr_full_rounds) + "/" + str(len(curr_completion_percentage)) + "\t" + str(int(100*curr_full_rounds/len(curr_completion_percentage))) + "%\t" + str(int(best_average)) + "%"
                subprocess.call("echo \"" + failed_tracks + "\" | aws s3 cp - s3://" + os.environ["SAGEMAKER_SHARED_S3_BUCKET"] + "/" + os.environ["SAGEMAKER_SHARED_S3_PREFIX"] + "/failed_tracks --content-type=text/plain", shell=True)

        print("Scheduling restart in " + str(restart_time) + " seconds ...")
        subprocess.Popen("sleep " + str(restart_time) + ";aws robomaker restart-simulation-job --job=\"$AWS_ROBOMAKER_SIMULATION_JOB_ARN\" --region=us-east-1", shell=True)
        print("Script done...")
    else:
        print("Skipping World Randomization in " + os.environ["JOB_TYPE"] + " Job")

    if os.environ["JOB_TYPE"] == "EVALUATION" and sys.argv[2] == "distributed_training.launch":
        print("Setting launch type to: evaluation.launch")
        sys.argv[2] = "evaluation.launch"

    print("World: " + os.environ["WORLD_NAME"])

randomize()