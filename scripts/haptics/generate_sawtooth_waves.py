import numpy as np
import scipy.io.wavfile as wavfile

def generate_inverse_sawtooth_wave(frequency, duration, sample_rate, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # 逆ノコギリ波の生成
    wave = amplitude * (2 * (t * frequency - np.floor(0.5 + t * frequency)))
    return wave

def generate_sawtooth_wave(frequency, duration, sample_rate, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # ノコギリ波の生成
    wave = amplitude * (2 * (np.floor(0.5 + t * frequency) - t * frequency))
    return wave

def save_wave(filename, wave, sample_rate):
    # WAVファイルに書き込む
    wavfile.write(filename, sample_rate, wave.astype(np.int16))

if __name__ == "__main__":
    frequency = 75        # 周波数（Hz）
    duration = 10         # 継続時間（秒）
    sample_rate = 44100   # サンプリングレート（Hz）
    amplitude = 32767     # 振幅 (16ビットPCMの最大値）

    inverse_sawtooth_wave = generate_inverse_sawtooth_wave(frequency, duration, sample_rate, amplitude)
    save_wave('inverse_sawtooth_wave.wav', inverse_sawtooth_wave, sample_rate)
    print("逆ノコギリ波のWAVファイルが生成されました。")

    sawtooth_wave = generate_sawtooth_wave(frequency, duration, sample_rate, amplitude)
    save_wave('sawtooth_wave.wav', sawtooth_wave, sample_rate)
    print("ノコギリ波のWAVファイルが生成されました。")