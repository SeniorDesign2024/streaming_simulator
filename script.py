import requests as fetch
from time import sleep
import json
import argparse
from sys import maxsize as maxInt
from sys import exit
from colorama import just_fix_windows_console
from termcolor import colored
import base64
import os
import random
import configparser
from typing import Union

def is_valid_integer_string(s):
  try:
    int(s)
    return True
  except ValueError:
    return False
    
def min_larger(dictionary, threshold):
  min_larger_key = float('inf')  # Initialize with positive infinity
  for key in dictionary:
    if key >= threshold and key < min_larger_key:
      min_larger_key = key
  return min_larger_key if min_larger_key != float('inf') else None

def proccessImage(imgPath: str, id: str, token: str):
  with open(imgPath, "rb") as imgFile:
    encodedImg = base64.b64encode(imgFile.read())
    encodedStr = "data:image/png;base64,"+encodedImg.decode("utf-8")

  payload = json.dumps({
    'event_id' : id,
    'image' : encodedStr
  })

  headers = {
    'Content-Type': 'application/json', 
    'x-access-token': token
    }

  try:
    res = fetch.post('http://localhost:3001/api/event/process-event', headers=headers, data=payload)
    if not res.ok:
      print(res.status_code)
      print(colored("ERR: Unable to process event. Please ensure you are using a valid EATwAI event id.", 'red'))
      exit(1)

  except fetch.exceptions.ConnectionError as e:
    print(colored("ERR: Unable to connect to server. Please ensure EATwAI server is running.", 'red'))
    exit(1)  # Exit the script with an error status code

def main():
  config = configparser.ConfigParser()
  config.read('config.ini')
  imagesDirPath = config.get('SETTINGS', 'images_path', fallback='./images')

  parser = argparse.ArgumentParser(description='Image test script')

  parser.add_argument('--username', '-u', type=str, default='test1', help='EATwAI username')
  parser.add_argument('--password', '-p', type=str, default='testPassword1', help='EATwAI password')
  parser.add_argument('--event', '-e', type=str, default='660d858b3b072376b8382c', help='EATwAI event Id(must match user)')
  parser.add_argument('--log', '-l', type=int, default='0', help='Print logs')
  parser.add_argument('--frames', '-f', type=int, default=maxInt, help='The number of frames to send, default is infinite')
  parser.add_argument('--rate', '-r', type=int, default=10000, help='The rate frames are sent in miliseconds')
  parser.add_argument('--method', '-m', type=str, default="wave_up", help='The method for which a picture will be chosen. Choices are "random", "increasing", "decreasing, "wave_up", "wave_down"')
  parser.add_argument('--growth', '-g', type=int, default=5, help='how fast the growth rate of the crowd')
  parser.add_argument('--individual', '-i',type=int, default=0, help='Send individual frames')

  args = parser.parse_args()
  username = args.username
  password = args.password
  event = args.event
  log = True if args.log == 1 else False
  frames = args.frames
  rate = args.rate
  method = args.method
  growth = args.growth
  individual = True if args.individual == 1 else False
  token = None

  if(method != 'random' and method != 'increasing' and method != 'decreasing' and method != 'wave_up' and method != 'wave_down'):
    print(colored('ERR: Method must be one of the following values : "random", "increasing", "decreasing, "waving_up", "waving_down".', 'red'))
    exit(1)

  if(log):
     print("Input:")
     print(colored(f"\tUsername : {username}\n\tPassword : {password}\n\tEvent Id : {event}", 'green'))

  payload = json.dumps({
      'username': username,
      'password': password
  })

  try:
    res = fetch.post('http://localhost:3001/api/auth/signin', headers={'Content-Type': 'application/json' }, data=payload)
    if not res.ok:
      print(colored("ERR: Unable to log into server. Please ensure you are using a valid EATwAI account.", 'red'))
      exit(1)

    body = res.json()
    token = body['accessToken']
    
  except fetch.exceptions.ConnectionError as e:
    print(colored("ERR: Unable to connect to server. Please ensure EATwAI server is running.", 'red'))
    exit(1)  # Exit the script with an error status code
  except json.decoder.JSONDecodeError as e:
    print(colored("ERR: Something went wrong signing into server", "red"))
    exit(1)

  files = os.listdir(imagesDirPath)
  if not files:
    print(colored("ERR: No image in ./images", "red"))
    exit(1)

  images = {}
  with open('./image_labels.txt', 'r') as file:
    for line in file:
        parts = line.strip().replace("'", "").split(',')
        value = int(parts[1])  # Extract the second value (as integer)
        key = parts[0] # Extract the first value
        # Check if the value is already in the dictionary
        if value in images:
            images[value].append(key)  # Append the key to the existing list
        else:
            images[value] = [key]  # Create a new list with the key as the only

  print("Count: Image Path")
  user_count = ""
  if(method == 'random'):
    while frames:
      if(individual):
        user_count = None
        while user_count == None:
          try:
            user_count = input()
          except KeyboardInterrupt:
            exit()
          if(user_count and is_valid_integer_string(user_count)):
            user_count = int(user_count)
          elif(user_count != ""):
            print(colored("Please enter a number", 'red'))
            user_count = None
        
      count = user_count if user_count else random.choice(list(images.keys()))
      image = random.choice(images[count])
      imagePath = os.path.join(imagesDirPath, image+'.jpg')
      if(log):
        print(colored(f'{count:04}: {imagePath}', 'green'))

      proccessImage(imagePath, event, token)
      frames -= 1
      if(not individual):
        sleep(rate/1000)
  else:
    i = 0 if method == 'increasing' or 'wave_up' else sorted(images.keys())[-1]
    direction = 1 if method == 'increasing' or 'wave_up' else -1
    while frames:
        if(individual):
          user_count = None
          while user_count == None:
            try:
              user_count = input()
            except KeyboardInterrupt:
              exit()
            if(user_count and is_valid_integer_string(user_count)):
              user_count = int(user_count)
            elif(user_count != ""):
              print(colored("Please enter a number", 'red'))
              user_count = None
        image = random.choice(images[user_count]) if user_count else random.choice(images[i])
        imagePath = os.path.join(imagesDirPath, image+'.jpg')
        if(log):
          print(colored(f'{i:04}: {imagePath}', 'green'))
        proccessImage(imagePath, event, token)
        
        direction = (direction if i+direction*growth > 0 and i+direction*growth <= sorted(images.keys())[-1] else \
                    (-1 if direction == 1 and i+direction*growth >= sorted(images.keys())[-1] else \
                    (1 if direction == -1 and i+direction*growth < 0 else -1))) if (method == "wave_up" or method == "wave_down") else \
                    (1 if method == 'increasing' else \
                    -1)
        
        frames -= 1

        i += (0 if i+direction*growth < 0 else \
              (sorted(images.keys())[-1] if i+direction*growth > sorted(images.keys())[-1] else \
              direction*growth))
        
        i = min_larger(images, i)
        if(not individual):
          sleep(rate/1000)

if __name__ == '__main__':
  just_fix_windows_console()
  main()