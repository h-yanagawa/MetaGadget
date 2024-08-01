import RPi.GPIO as GPIO
import sys
from metagadget import MetaGadget

# ピンの設定
FAN1_PIN = 18
FAN2_PIN = 19

# PWMの周波数
FREQUENCY = 1000

# GPIOの初期設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN1_PIN, GPIO.OUT)
GPIO.setup(FAN2_PIN, GPIO.OUT)

pwm_fan1 = GPIO.PWM(FAN1_PIN, FREQUENCY)
pwm_fan2 = GPIO.PWM(FAN2_PIN, FREQUENCY)

pwm_fan1.start(0)
pwm_fan2.start(0)

def set_fan_duty_cycle(pwm, duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)

def main():
    app = MetaGadget()

    @app.receive
    def handle(data):
        try:
            fan1_duty, fan2_duty = map(float, data.split())
        except ValueError:
            print("入力が不正です。2つの数値をスペースで区切って入力してください。")
            return

        if 0 <= fan1_duty <= 100:
            set_fan_duty_cycle(pwm_fan1, fan1_duty)
        else:
            print("ファン1のデューティー比は0から100の間で入力してください。")

        if 0 <= fan2_duty <= 100:
            set_fan_duty_cycle(pwm_fan2, fan2_duty)
        else:
            print("ファン2のデューティー比は0から100の間で入力してください。")

    app.run()

    pwm_fan1.stop()
    pwm_fan2.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    main()
