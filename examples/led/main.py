import RPi.GPIO as GPIO
from metagadget import MetaGadget

# PIN Number
LED_PIN = 14

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


def main():
    app = MetaGadget()

    @app.receive
    def handle(data):
        if data == "on":
            GPIO.output(LED_PIN, 1)
        else:
            GPIO.output(LED_PIN, 0)

    app.run()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
