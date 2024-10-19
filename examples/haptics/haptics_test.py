import os
import pygame
import RPi.GPIO as GPIO
import sys

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
    audio_dir = 'data'
    quit_flag = False

    try:
        while True:
            files = list_audio_files(audio_dir)
            user_input = input("再生する音声ファイルの番号を入力してください ('q'で終了): ")
            
            if user_input.lower() == 'q':
                if quit_flag:
                    print("プログラムを終了します。")
                    break
                else:
                    quit_flag = True
                    continue

            try:
                file_index = int(user_input) - 1
                if 0 <= file_index < len(files):
                    file_path = os.path.join(audio_dir, files[file_index])
                    print(f"{files[file_index]} を再生します。")

                    while True:
                        try:
                            volume_input = input("再生音量を入力してください (0から100) ('q'で終了): ")
                            if volume_input.lower() == 'q':
                                print("再生を停止します。")
                                stop_audio()
                                GPIO.output(LED_PIN, GPIO.LOW)
                                break

                            volume = int(volume_input)
                            if 0 <= volume <= 100:
                                GPIO.output(LED_PIN, GPIO.HIGH)
                                play_audio_file(file_path, volume)
                                quit_flag = False
                            else:
                                print("音量は0から100の範囲で入力してください。")
                        except ValueError:
                            print("音量は0から100の範囲で入力してください。")
            except ValueError:
                print("入力が不正です。番号を入力してください。")

    except KeyboardInterrupt:
        pass

    finally:
        stop_audio()
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()
        pygame.mixer.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()
