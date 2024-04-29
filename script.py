import requests as fetch
import json
import argparse
import os
import base64
import time

def process_image(img_path: str, id: str, token: str):
    with open(img_path, "rb") as imgFile:
        encodedImg = base64.b64encode(imgFile.read())
        encodedStr = "data:image/jpeg;base64,"+encodedImg.decode("utf-8")

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
            print("ERR: Unable to process event. Please ensure you are using a valid EATwAI event id.")
            exit(1)

    except fetch.exceptions.ConnectionError as e:
        print("ERR: Unable to connect to server. Please ensure EATwAI server is running.")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description='Image test script')

    parser.add_argument('--username', '-u', type=str, default='demo', help='EATwAI username')
    parser.add_argument('--password', '-p', type=str, default='thisistest3', help='EATwAI password')
    parser.add_argument('--event', '-e', type=str, default='66245b4f0414180e35f9681d', help='EATwAI event Id(must match user)')
    parser.add_argument('--rate', '-r', type=int, default=10000, help='The rate frames are sent in milliseconds')
    parser.add_argument('--images-dir', '-i', type=str, default='./images', help='Directory path where images are stored')

    args = parser.parse_args()
    username = args.username
    password = args.password
    event_id = args.event
    rate = args.rate
    images_dir = args.images_dir
    token = None

    payload = json.dumps({
        'username': username,
        'password': password
    })

    try:
        res = fetch.post('http://localhost:3001/api/auth/signin', headers={'Content-Type': 'application/json'}, data=payload)
        if not res.ok:
            print("ERR: Unable to log into server. Please ensure you are using a valid EATwAI account.")
            exit(1)

        body = res.json()
        token = body['accessToken']

    except fetch.exceptions.ConnectionError as e:
        print("ERR: Unable to connect to server. Please ensure EATwAI server is running.")
        exit(1)
    except json.decoder.JSONDecodeError as e:
        print("ERR: Something went wrong signing into server")
        exit(1)

    image_files = [file for file in os.listdir(images_dir) if file.startswith('IMG_')]
    if not image_files:
        print("ERR: No image files found in the specified directory.")
        exit(1)

    print("Sending images for processing...")
    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        process_image(image_path, event_id, token)
        time.sleep(rate / 1000)

if __name__ == '__main__':
    main()