import wave, numpy as np
from PIL import Image, ImageDraw

W, H = 1280, 60
N_BARS = 256
BAR_W = W // N_BARS  # 5px per bar
CENTER_Y = H // 2
MAX_BAR_H = H // 2 - 2

with wave.open('work/audio.wav', 'rb') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    n_frames = wf.getnframes()
    raw = wf.readframes(n_frames)

if sampwidth == 2:
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
elif sampwidth == 4:
    samples = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
else:
    samples = np.frombuffer(raw, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0

if n_channels == 2:
    samples = samples.reshape(-1, 2).mean(axis=1)

chunk = max(1, len(samples) // N_BARS)
amps = []
for i in range(N_BARS):
    c = samples[i * chunk:(i + 1) * chunk]
    amps.append(float(np.sqrt(np.mean(c ** 2))) if len(c) > 0 else 0.0)

peak = max(amps) or 1.0
amps = [a / peak for a in amps]

img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

for i, amp in enumerate(amps):
    x = i * BAR_W
    bar_h = max(2, int(amp * MAX_BAR_H))
    # cyan (#4af0ff) with alpha proportional to amplitude
    alpha = int(120 + 135 * amp)
    draw.rectangle(
        [x, CENTER_Y - bar_h, x + BAR_W - 1, CENTER_Y + bar_h],
        fill=(74, 240, 255, alpha)
    )

img.save('work/waveform.png')
print(f'waveform.png generated: {W}x{H}, {N_BARS} bars')
