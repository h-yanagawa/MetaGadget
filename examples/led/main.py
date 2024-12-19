import RPi.GPIO as GPIO
from metagadget import MetaGadget

# PIN Number
LED_PIN = 14

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


def main():
    """Initialize and run the MetaGadget LED control application.

    Creates a MetaGadget instance and sets up an LED control handler that
    responds to 'on' and 'off' commands from the metaverse platform.
    """
    app = MetaGadget()

    @app.receive
    def handle(data):
        """Handle incoming LED control commands.

        Args:
            data: String command, either 'on' or 'off' to control LED state.
        """
        if data == "on":
            GPIO.output(LED_PIN, 1)
        else:
            GPIO.output(LED_PIN, 0)

    app.run()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
