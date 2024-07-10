import RPi.GPIO as GPIO
import sys

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
    try:
        while True:
            user_input = input("ファン1とファン2のデューティー比 (0から100) をスペースで区切って入力 ('q'で終了): ")
            if user_input.lower() == 'q':
                print("qキーが押されました。プログラムを終了します。")
                pwm_fan1.stop()
                pwm_fan2.stop()
                GPIO.cleanup()
                sys.exit(0)

            try:
                fan1_duty, fan2_duty = map(float, user_input.split())
                if 0 <= fan1_duty <= 100 and 0 <= fan2_duty <= 100:
                    set_fan_duty_cycle(pwm_fan1, fan1_duty)
                    set_fan_duty_cycle(pwm_fan2, fan2_duty)
                else:
                    print("デューティー比は0から100の間で入力してください。")
            except ValueError:
                print("入力が不正です。2つの数値をスペースで区切って入力してください。")
    except KeyboardInterrupt:
        pwm_fan1.stop()
        pwm_fan2.stop()
        GPIO.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    main()
