from flask import Flask
from flask import request
import ngrok
import RPi.GPIO as GPIO

import os
import time
import json


FREQUENCY = 1
GPIONUM = 29

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIONUM, GPIO.OUT)
GPIO.output(GPIONUM, GPIO.HIGH)


def up():
    GPIO.output(GPIONUM, GPIO.LOW)


def down():
    GPIO.output(GPIONUM, GPIO.HIGH)


app = Flask(__name__)


@app.route("/", methods=["POST"])
def root():
    data = json.loads(request.get_json()['request'])
    print(f"Diff {time.time() * 1000 - data['time']:.2f} millseconds")
    if data['isGrab'] == 1:
        up()
    else:
        down()
    return "Hello, World!"


if __name__ == "__main__":
    PORT = 5001
    DOMAIN = os.environ.get("NGROK_DOMAIN")
    ngrok.forward(PORT, authtoken_from_env=True, domain=DOMAIN)
    app.run(host='0.0.0.0', port=PORT)
    down()
    GPIO.cleanup()
