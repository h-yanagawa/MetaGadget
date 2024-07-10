import RPi.GPIO as GPIO
import sys
from metagadget import MetaGadget

# ピンの設定
PEL_L_PHASE = 17
PEL_L_ENABLE = 18
PEL_R_PHASE = 27
PEL_R_ENABLE = 19
FAN_L = 22
FAN_R = 23
PEL_STANDBY = 24

# PWMの周波数
FREQUENCY = 1000

# GPIOの初期設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PEL_L_PHASE, GPIO.OUT)
GPIO.setup(PEL_L_ENABLE, GPIO.OUT)
GPIO.setup(PEL_R_PHASE, GPIO.OUT)
GPIO.setup(PEL_R_ENABLE, GPIO.OUT)
GPIO.setup(FAN_L, GPIO.OUT)
GPIO.setup(FAN_R, GPIO.OUT)
GPIO.setup(PEL_STANDBY, GPIO.OUT)

# ペルチェのスタンバイピンをHighに設定
GPIO.output(PEL_STANDBY, GPIO.HIGH)

pwm_pel_l = GPIO.PWM(PEL_L_ENABLE, FREQUENCY)
pwm_pel_r = GPIO.PWM(PEL_R_ENABLE, FREQUENCY)
pwm_fan_l = GPIO.PWM(FAN_L, FREQUENCY)
pwm_fan_r = GPIO.PWM(FAN_R, FREQUENCY)

pwm_pel_l.start(0)
pwm_pel_r.start(0)
pwm_fan_l.start(0)
pwm_fan_r.start(0)


def set_peltier(pwm, phase_pin, duty_cycle):
    if duty_cycle >= 0:
        GPIO.output(phase_pin, GPIO.LOW)  # 加熱
    else:
        GPIO.output(phase_pin, GPIO.HIGH)   # 冷却
        duty_cycle = -duty_cycle  # デューティー比を正の値に変換
    pwm.ChangeDutyCycle(duty_cycle)


def main():
    app = MetaGadget()

    @app.receive
    def hundle(data):
        try:
            left_duty, right_duty = map(float, data.split())
        except ValueError:
            print("入力が不正です。2つの数値をスペースで区切って入力してください。")
            return

        set_peltier(pwm_pel_l, PEL_L_PHASE, left_duty)
        set_peltier(pwm_pel_r, PEL_R_PHASE, right_duty)

        # ファンの制御
        if left_duty != 0:
            pwm_fan_l.ChangeDutyCycle(100)  # 左ペルチェが駆動中ならファンを100%で動作
        else:
            pwm_fan_l.ChangeDutyCycle(0)

        if right_duty != 0:
            pwm_fan_r.ChangeDutyCycle(100)  # 右ペルチェが駆動中ならファンを100%で動作
        else:
            pwm_fan_r.ChangeDutyCycle(0)

    app.run()

    pwm_pel_l.stop()
    pwm_pel_r.stop()
    pwm_fan_l.stop()
    pwm_fan_r.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    main()
