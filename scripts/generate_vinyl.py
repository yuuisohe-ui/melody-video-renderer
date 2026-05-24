import sys
import os
from PIL import Image, ImageDraw
import math

def generate_vinyl_image(song_title, cover_path, output_path, width=1280, height=720):
    img = Image.new('RGB', (width, height), (10, 8, 16))
    draw = ImageDraw.Draw(img)

    vinyl_r = 500
    cx = int(vinyl_r * 0.15)
    cy = height // 2
    label_r = 280
    cover_r = 240

    # 背景渐变（用矩形模拟）
    for i in range(width):
        ratio = i / width
        r = int(26 + (8-26)*ratio)
        g = int(16 + (8-16)*ratio)
        b = int(53 + (16-53)*ratio)
        draw.line([(i, 0), (i, height)], fill=(r, g, b))

    # 紫色光晕
    glow = Image.new('RGBA', (width, height), (0,0,0,0))
    glow_draw = ImageDraw.Draw(glow)
    for r_step in range(200, 0, -1):
        alpha = int(60 * (1 - r_step/200))
        glow_draw.ellipse([cx-r_step, cy-r_step, cx+r_step, cy+r_step],
                         fill=(64, 32, 160, alpha))
    img.paste(Image.alpha_composite(Image.new('RGBA', (width,height),(0,0,0,0)), glow).convert('RGB'),
              mask=glow.split()[3])

    # 唱片主体
    draw.ellipse([cx-vinyl_r, cy-vinyl_r, cx+vinyl_r, cy+vinyl_r],
                fill=(22, 22, 22))

    # 凹槽
    for i in range(6, 48):
        r = int(vinyl_r * (0.35 + i * 0.013))
        if r > vinyl_r - 10:
            break
        color = (80, 80, 80) if i % 5 == 0 else (50, 50, 50)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=1)

    # 金色标签
    label_colors = [(240,208,112),(212,168,75),(184,136,46),(122,90,26)]
    for idx, lc in enumerate(label_colors):
        lr = label_r - idx * (label_r//4)
        if lr > 0:
            draw.ellipse([cx-lr, cy-lr, cx+lr, cy+lr], fill=lc)

    # 封面图（圆形裁剪）
    if cover_path and os.path.exists(cover_path):
        try:
            cover = Image.open(cover_path).convert('RGBA')
            cover = cover.resize((cover_r*2, cover_r*2), Image.LANCZOS)
            
            # 圆形蒙版
            mask = Image.new('L', (cover_r*2, cover_r*2), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, cover_r*2, cover_r*2], fill=255)
            
            # 粘贴封面图
            cover_x = cx - cover_r
            cover_y = cy - cover_r
            img.paste(cover, (cover_x, cover_y), mask)
        except Exception as e:
            print(f"Cover image error: {e}")

    # 中心孔
    hole_r = max(6, int(vinyl_r * 0.022))
    draw.ellipse([cx-hole_r, cy-hole_r, cx+hole_r, cy+hole_r], fill=(10,10,10))

    # 唱臂
    pivot_x = cx + vinyl_r + 60
    pivot_y = 70
    needle_x = cx + int(vinyl_r * 0.55)
    needle_y = cy - int(vinyl_r * 0.28)

    draw.line([(pivot_x, pivot_y), (needle_x, needle_y)],
              fill=(201,169,110), width=8)
    draw.ellipse([needle_x-6, needle_y-6, needle_x+6, needle_y+6],
                fill=(201,169,110))

    # 支点
    pivot_r_size = 18
    draw.ellipse([pivot_x-pivot_r_size, pivot_y-pivot_r_size,
                  pivot_x+pivot_r_size, pivot_y+pivot_r_size],
                fill=(212,168,75))
    draw.ellipse([pivot_x-pivot_r_size, pivot_y-pivot_r_size,
                  pivot_x+pivot_r_size, pivot_y+pivot_r_size],
                outline=(201,169,110), width=2)
    draw.ellipse([pivot_x-5, pivot_y-5, pivot_x+5, pivot_y+5],
                fill=(51,51,51))

    # 分隔线
    right_start = cx + vinyl_r + 40
    draw.line([(right_start, 80), (right_start, height-80)],
              fill=(51,51,51), width=1)

    # 歌曲名
    try:
        from PIL import ImageFont
        font_paths = [
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
            '/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
        ]
        font_large = None
        font_small = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_large = ImageFont.truetype(fp, 28)
                font_small = ImageFont.truetype(fp, 13)
                break
        if font_large:
            draw.text((right_start+40, height-90), "LYRIC VIDEO",
                     fill=(136,136,136), font=font_small)
            draw.text((right_start+40, height-55), song_title,
                     fill=(255,255,255), font=font_large)
        else:
            draw.text((right_start+40, height-90), "LYRIC VIDEO", fill=(136,136,136))
            draw.text((right_start+40, height-55), song_title, fill=(255,255,255))
    except Exception as e:
        print(f"Font error: {e}")
        draw.text((right_start+40, height-55), song_title, fill=(255,255,255))

    img.save(output_path, 'PNG', quality=95)
    print(f"Image generated: {output_path}")

if __name__ == "__main__":
    song_title = sys.argv[1] if len(sys.argv) > 1 else "AI 노래"
    cover_path = sys.argv[2] if len(sys.argv) > 2 else "work/cover.jpg"
    output = sys.argv[3] if len(sys.argv) > 3 else "work/vinyl_bg.png"
    generate_vinyl_image(song_title, cover_path, output)
