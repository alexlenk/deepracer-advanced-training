# DeepRacer Advanced Training for AWS DeepRacer Console

This project provides helping scripts to automate the training of DeepRacer models using the official AWS DeepRacer console for re-inforcement learning.

# Installation
1. Start a new DeepRacer job
2. Get the Robomaker ARN from the Robomaker Console
3. execute ./increase_speed.py <robomaker arn> <time in minutes> <percentage increase> (e.g. ./increase_speed.py "arn:aws:robomaker:us-east-1:000000000:simulation-job/sim-6z3jfvryz3dh" 120 1.10)
