import sys
import os
import math

def generate_vinyl_svg(cover_url, output_path, width=1280, height=720):
    # 唱片参数
    vinyl_r = 420  # 唱片半径，故意很大
    cx = -80       # 圆心X，负数让左边切掉
    cy = height // 2  # 圆心Y，垂直居中
    
    label_r = int(vinyl_r * 0.27)   # 金色标签半径
    cover_r = int(label_r * 0.85)   # 封面图半径（比标签小）
    
    # 生成唱片凹槽
    grooves = ""
    for i in range(6, 48):
        r = vinyl_r * (0.35 + i * 0.013)
        if r > vinyl_r - 10:
            break
        opacity = 0.032 if i % 5 == 0 else 0.012
        color = "#666666" if i % 5 == 0 else "#444444"
        grooves += f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="0.8" opacity="{opacity}"/>\n'
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- 배경 그라디언트 -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a1035"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </linearGradient>
    
    <!-- 바이닐 그라디언트 -->
    <radialGradient id="vinylGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#252525"/>
      <stop offset="40%" stop-color="#181818"/>
      <stop offset="100%" stop-color="#0c0c0c"/>
    </radialGradient>
    
    <!-- 금색 라벨 그라디언트 -->
    <radialGradient id="labelGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#e8c870"/>
      <stop offset="40%" stop-color="#d4a84b"/>
      <stop offset="70%" stop-color="#b8882e"/>
      <stop offset="100%" stop-color="#7a5a1a"/>
    </radialGradient>

    <!-- 커버 이미지 클립 -->
    <clipPath id="coverClip">
      <circle cx="{cx}" cy="{cy}" r="{cover_r}"/>
    </clipPath>

    <!-- 唱臂渐变 -->
    <linearGradient id="armGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#c9a96e"/>
      <stop offset="50%" stop-color="#e8c870"/>
      <stop offset="100%" stop-color="#c9a96e"/>
    </linearGradient>
    
    <!-- 支点渐变 -->
    <radialGradient id="pivotGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#e8c870"/>
      <stop offset="100%" stop-color="#8a6520"/>
    </radialGradient>

    <!-- 바이닐 글로우 -->
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- 배경 -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)"/>
  
  <!-- 바이닐 글로우 -->
  <ellipse cx="{cx}" cy="{cy}" rx="{vinyl_r}" ry="{vinyl_r}" fill="url(#glowGrad)"/>
  
  <!-- 바이닐 본체 -->
  <circle cx="{cx}" cy="{cy}" r="{vinyl_r}" fill="url(#vinylGrad)"/>
  
  <!-- 바이닐 외곽 테두리 -->
  <circle cx="{cx}" cy="{cy}" r="{vinyl_r - 3}" fill="none" stroke="#333333" stroke-width="1.5"/>
  
  <!-- 凹槽 -->
  {grooves}
  
  <!-- 금색 라벨 -->
  <circle cx="{cx}" cy="{cy}" r="{label_r}" fill="url(#labelGrad)"/>
  
  <!-- 라벨 하이라이트 -->
  <ellipse cx="{cx - label_r*0.2}" cy="{cy - label_r*0.25}" rx="{label_r*0.4}" ry="{label_r*0.25}" 
           fill="white" opacity="0.12"/>
  
  <!-- 封面图 -->
  <image href="{cover_url}" 
         x="{cx - cover_r}" y="{cy - cover_r}" 
         width="{cover_r * 2}" height="{cover_r * 2}"
         clip-path="url(#coverClip)"
         preserveAspectRatio="xMidYMid slice"/>
  
  <!-- 중심 구멍 -->
  <circle cx="{cx}" cy="{cy}" r="{vinyl_r * 0.025:.1f}" fill="#0a0a0a"/>

  <!-- 唱臂 支点位置 -->
  <g transform="translate({width * 0.72:.0f}, {height * 0.12:.0f})">
    <!-- 支点圆盘 -->
    <circle cx="0" cy="0" r="{width * 0.035:.0f}" fill="url(#pivotGrad)"/>
    <circle cx="0" cy="0" r="{width * 0.035:.0f}" fill="none" stroke="#c9a96e" stroke-width="1.5"/>
    <!-- 高光 -->
    <ellipse cx="{-width*0.01:.0f}" cy="{-height*0.018:.0f}" 
             rx="{width*0.012:.0f}" ry="{height*0.01:.0f}" 
             fill="white" opacity="0.25"/>
    
    <!-- 唱臂 旋转约 0.34 弧度 (约20度) -->
    <g transform="rotate(-20)">
      <!-- 臂身 贝塞尔曲线 -->
      <path d="M 0 0 Q {-width*0.06:.0f} {height*0.25:.0f} {-width*0.16:.0f} {height*0.52:.0f}" 
            fill="none" stroke="url(#armGrad)" stroke-width="{width*0.008:.0f}" 
            stroke-linecap="round"/>
      <!-- 针두 -->
      <ellipse cx="{-width*0.164:.0f}" cy="{height*0.525:.0f}" 
               rx="{width*0.018:.0f}" ry="{height*0.012:.0f}" 
               fill="#c9a96e" transform="rotate(-15 {-width*0.164:.0f} {height*0.525:.0f})"/>
    </g>
  </g>

</svg>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"SVG generated: {output_path}")

if __name__ == "__main__":
    cover_url = sys.argv[1] if len(sys.argv) > 1 else ""
    output = sys.argv[2] if len(sys.argv) > 2 else "work/vinyl.svg"
    generate_vinyl_svg(cover_url, output)
