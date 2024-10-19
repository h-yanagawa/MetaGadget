import os
import pygame
import RPi.GPIO as GPIO
import sys
from metagadget import MetaGadget
import time
# GPIO設定
LED_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# pygame初期化
pygame.mixer.init()

def list_audio_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.wav')]
    for i, file in enumerate(files, start=1):
        print(f"{i}: {file}")
    return files

def play_audio_file(file_path, volume):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume / 100.0)
    pygame.mixer.music.play(-1)  # ループ再生

def stop_audio():
    pygame.mixer.music.stop()

def main():
    app = MetaGadget()
    audio_dir = 'data'
    
    @app.receive
    def handle(data):
        try:
            file_index, volume = map(int, data.split())
        except ValueError:
            print("入力が不正です。ファイル番号と音量をスペースで区切って入力してください。")
            return

        files = list_audio_files(audio_dir)
        
        if 0 <= file_index - 1 < len(files):
            file_path = os.path.join(audio_dir, files[file_index - 1])
            if 0 <= volume <= 100:
                print(f"{files[file_index - 1]} を音量 {volume} で再生します。")
                GPIO.output(LED_PIN, GPIO.HIGH)
                play_audio_file(file_path, volume)
                time.sleep(3)
                stop_audio()
            else:
                print("音量は0から100の範囲で入力してください。")
        else:
            print("ファイル番号が無効です。")

    app.run()

    stop_audio()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
    pygame.mixer.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
