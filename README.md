# Streaming Simulator
This Repo is used to test the machine learning algorithm used to do crowd counting.

## Installation
To install requirements run:
```bash
pip install -r requirements.txt
```
You also need to download the images to use this. To download the images go to the shared google drive `EATwAI` and download the images zip drive. Unzip this in the root directory of the repo and run!

## How to run
To see all help commands run
```bash
python script.py -h
```

Here are some examples
```bash
python script.py -l 1 -r 5000 -f 25 -g 10
```
In this example it `-l` will show logs `-r 5000` will send frames every 5 seconds. `-f 25` will send only 25 frames before ending. `-g 10` Will increase the number of individuals in the frames at a rate of 10 people per new frame.

```bash
python script.py -l 1 -i 1
```
This let's you send individual frames manual. You an either hit enter to use the default mode of generation or enter the number of people you would like to see in the frame.

## Density Branch (Another testing script)
To access this branch, `git checkout density`.

Follow this steps for setup:
- Create an folder called `images` in the root directory.    
- Paste the images you want to calculate count for.    
- There is currently an example user and event for which you can test. If you wish to change, modify the code with another correct username, password, and eventid. It can be found in the database.    
- run `python script.py` or `python3 script.py`.    
- The result will be displayed on the frontend web application.    
