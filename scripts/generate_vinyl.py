import sys
import os
import base64

def image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{data}"
    except:
        return ""

def generate_vinyl_svg(song_title, output_path, width=1280, height=720):
    vinyl_r = 380
    cx = int(vinyl_r * 0.2)
    cy = height // 2

    label_r = int(vinyl_r * 0.28)
    cover_r = int(label_r * 0.82)

    pivot_x = cx + vinyl_r + 60
    pivot_y = 70
    pivot_r = 14

    needle_x = cx + int(vinyl_r * 0.55)
    needle_y = cy - int(vinyl_r * 0.28)

    grooves = ""
    for i in range(6, 48):
        r = vinyl_r * (0.35 + i * 0.013)
        if r > vinyl_r - 10:
            break
        opacity = 0.04 if i % 5 == 0 else 0.015
        color = "#777777" if i % 5 == 0 else "#444444"
        grooves += f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="0.8" opacity="{opacity}"/>\n'

    cover_data = image_to_base64("work/cover.jpg")
    cover_img = ""
    if cover_data:
        cover_img = f'''
  <image href="{cover_data}"
         x="{cx - cover_r}" y="{cy - cover_r}"
         width="{cover_r * 2}" height="{cover_r * 2}"
         clip-path="url(#coverClip)"
         preserveAspectRatio="xMidYMid slice"/>'''

    right_start = cx + vinyl_r + 40

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a1035"/>
      <stop offset="100%" stop-color="#080810"/>
    </linearGradient>
    <radialGradient id="vinylGrad" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#2a2a2a"/>
      <stop offset="50%" stop-color="#161616"/>
      <stop offset="100%" stop-color="#080808"/>
    </radialGradient>
    <radialGradient id="labelGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#f0d080"/>
      <stop offset="35%" stop-color="#d4a84b"/>
      <stop offset="70%" stop-color="#b8882e"/>
      <stop offset="100%" stop-color="#7a5a1a"/>
    </radialGradient>
    <radialGradient id="pivotGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#f0d080"/>
      <stop offset="100%" stop-color="#8a6520"/>
    </radialGradient>
    <linearGradient id="armGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c9a96e"/>
      <stop offset="40%" stop-color="#e8c870"/>
      <stop offset="100%" stop-color="#a07830"/>
    </linearGradient>
    <radialGradient id="glowGrad" cx="30%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4020a0" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#4020a0" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="coverClip">
      <circle cx="{cx}" cy="{cy}" r="{cover_r}"/>
    </clipPath>
  </defs>

  <!-- 배경 -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)"/>
  <ellipse cx="{cx}" cy="{cy}" rx="{vinyl_r + 60}" ry="{vinyl_r + 60}" fill="url(#glowGrad)"/>

  <!-- 바이닐 -->
  <circle cx="{cx}" cy="{cy}" r="{vinyl_r}" fill="url(#vinylGrad)"/>
  <circle cx="{cx}" cy="{cy}" r="{vinyl_r - 2}" fill="none" stroke="#3a3a3a" stroke-width="2"/>
  {grooves}

  <!-- 금색 라벨 -->
  <circle cx="{cx}" cy="{cy}" r="{label_r}" fill="url(#labelGrad)"/>
  <ellipse cx="{cx - int(label_r*0.18)}" cy="{cy - int(label_r*0.22)}"
           rx="{int(label_r*0.38)}" ry="{int(label_r*0.22)}"
           fill="white" opacity="0.15"/>

  <!-- 封面图 (base64) -->
  {cover_img}

  <!-- 중심 구멍 -->
  <circle cx="{cx}" cy="{cy}" r="{max(6, int(vinyl_r * 0.022))}" fill="#0a0a0a"/>
  <circle cx="{cx}" cy="{cy}" r="{max(3, int(vinyl_r * 0.01))}" fill="#222222"/>

  <!-- 唱臂 -->
  <line x1="{pivot_x}" y1="{pivot_y}"
        x2="{needle_x}" y2="{needle_y}"
        stroke="url(#armGrad)" stroke-width="8" stroke-linecap="round"/>
  <circle cx="{needle_x}" cy="{needle_y}" r="6" fill="#c9a96e"/>

  <!-- 支点 -->
  <circle cx="{pivot_x}" cy="{pivot_y}" r="{pivot_r}" fill="url(#pivotGrad)"/>
  <circle cx="{pivot_x}" cy="{pivot_y}" r="{pivot_r}" fill="none" stroke="#c9a96e" stroke-width="1.5"/>
  <ellipse cx="{pivot_x - 4}" cy="{pivot_y - 5}" rx="6" ry="4" fill="white" opacity="0.25"/>
  <circle cx="{pivot_x}" cy="{pivot_y}" r="4" fill="#333"/>

  <!-- 구분선 -->
  <line x1="{right_start}" y1="80" x2="{right_start}" y2="{height - 80}"
        stroke="#333333" stroke-width="1"/>

  <!-- 歌曲名 -->
  <text x="{right_start + 40}" y="{height - 80}"
        fill="#888888" font-size="13"
        font-family="Noto Sans CJK SC, sans-serif"
        letter-spacing="3">LYRIC VIDEO</text>
  <text x="{right_start + 40}" y="{height - 48}"
        fill="#ffffff" font-size="28" font-weight="bold"
        font-family="Noto Sans CJK SC, sans-serif">{song_title}</text>

  <!-- 진행 바 -->
  <rect x="{right_start + 40}" y="{height - 18}"
        width="{width - right_start - 80}" height="2"
        fill="#333333" rx="1"/>

</svg>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"SVG generated: {output_path}")

if __name__ == "__main__":
    song_title = sys.argv[1] if len(sys.argv) > 1 else "AI 노래"
    output = sys.argv[2] if len(sys.argv) > 2 else "work/vinyl.svg"
    generate_vinyl_svg(song_title, output)
