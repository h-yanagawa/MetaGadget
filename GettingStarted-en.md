# MetaGadget Getting Started

# Preparing the device

Let's prepare a physical device to connect to the cluster using MetaGadget.

For this project, we'll use a Raspberry Pi Zero 2 W as our microcomputer and control an LED through GPIO. The end result will be a gadget where interacting with a light bulb (tapping on screen) in the cluster will light up a real LED.

# Connecting Raspberry Pi Zero 2 W and LED

Set up the circuit as shown in the figure.

![circuit](https://github.com/user-attachments/assets/cdf78993-5c05-4ee5-b4da-3e92afdb4d1b)

# Setting up Raspberry Pi Zero 2 W

From here on, we'll proceed assuming that Raspberry Pi OS Lite is already installed.

Please refer to this guide for instructions on installing Raspberry Pi OS Lite.

Installing required packages

```bash
sudo apt-get install vim python3-dev

python -m venv venv
. venv/bin/activate
pip install metagadget RPi.GPIO
```

# Getting an ngrok account

To run MetaGadget, you'll need an ngrok account. You can create one for free at [this link](https://ngrok.com/). After creating an account, obtain your Auth Token and your account-linked domain from the management dashboard.

# Preparing a Python program to receive Call External from Cluster

Now that the setup is complete, let's prepare a program using the MetaGadget library.

```python
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
```

Start the program with the following environment variables. These environment variables are necessary for ngrok configuration. Specify the Auth Token and domain you obtained when creating your ngrok account.

```bash
NGROK_AUTHTOKEN="YOUR_NGROK_KEY"  NGROK_DOMAIN="YOUR_NGROK_DOMAIN" python main.py

WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

If you see the above message, the program is running.

Before checking with cluster, let's verify the operation using curl. The following command will turn on the LED:

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"request": "on"}' https://YOUR_NGROK_DOMAIN/
```

Now let's turn off the LED:

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"request": "off"}' https://YOUR_NGROK_DOMAIN/
```

If the LED doesn't light up, check if the LED circuit is properly connected. Also, check if there are any error messages in the Raspberry Pi shell.

# Creating a Craft Item

Let's create a Craft Item in Unity with Cluster Creator Kit set up.

First, we'll register a simple sphere as an Item.

Create an Empty Game Object and name it "Light".

Create a Sphere under it. The Hierarchy screen should look like this:

![hierachy](https://github.com/user-attachments/assets/20ccbed9-fbf2-41e7-8994-a00355da2f0c)

In the Scene view, only the Sphere will be visible.

![scene](https://github.com/user-attachments/assets/7ee41a28-d077-4f09-8e88-4a40ca0a30e3)

Add "Item(Script)" and "Scriptable Item (Script)" components from the Inspector window of the Light object (Empty GameObject). Don't forget to specify the Item Name and Size in the "Item(Script)" component settings. In "Scriptable Item (Script)", you can set the Cluster Script linked to this object, but we'll set it later, so it's fine to leave it empty for now.

![inspector](https://github.com/user-attachments/assets/1704dee1-fde7-408b-be31-aa7d1697f76b)

Once the item is created, it needs to be uploaded. Select Cluster > UploadCraftItem from the menu to open the settings screen.

![UploadCraftItem](https://github.com/user-attachments/assets/69ae8f5a-c5f0-4c18-b310-200298420ad6)

You can register the Item by dragging and dropping the prefabbed item onto this screen. If it shows "Valid Item", press Upload to register your created item.

Then, register the callExternal destination from the Unity menu. Select Cluster > ExternalCommunication from the menu to open the settings screen. Register the URL in the format "https://YOUR_NGROK_DOMAIN/" using your ngrok domain obtained earlier.

![ExternalCommunication](https://github.com/user-attachments/assets/98134e7b-5ea7-4681-a6d5-be4c209e05c3)

# Placing the Craft Item

Let's place the created item in your world craft.

![putItem](https://github.com/user-attachments/assets/e2d0985d-f0e9-4b8a-b26b-a66364274064)

Since this item doesn't have a script registered, press F12 to edit the script while the item is selected in craft mode.

```bash
let ledOn = false;
$.onInteract(() => {
  $.log("interacted.");
  if (ledOn) {
    ledOn = false;
    $.callExternal("off", "led");
  } else {
    ledOn = true;
    $.callExternal("on", "led");
  }
});

$.onExternalCallEnd((res, meta, err) => {
  $.log("external call end.");
  $.log(res); // Display response for debugging
  $.log(meta); // Display meta information specified at request time. Will show "led"
  $.log(err); // If an error occurs, this code will display the error
});
```

After registering this script to the item, you can control the LED's on/off state by clicking the sphere.

Now you've completed implementing the entire flow of controlling a real device from a Craft Item using MetaGadget.
