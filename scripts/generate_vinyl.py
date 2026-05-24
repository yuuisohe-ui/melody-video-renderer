import sys
import os
from PIL import Image, ImageDraw

def generate_vinyl_image(song_title, cover_path, output_path, width=1280, height=720):
    img = Image.new('RGB', (width, height), (10, 8, 16))
    draw = ImageDraw.Draw(img)

    # 背景渐变
    for i in range(width):
        ratio = i / width
        r = int(26 + (8-26)*ratio)
        g = int(16 + (8-16)*ratio)
        b = int(53 + (16-53)*ratio)
        draw.line([(i, 0), (i, height)], fill=(r, g, b))

    vinyl_r = 500
    cx = int(vinyl_r * 0.15)
    cy = height // 2
    label_r = 280
    cover_r = 240

    # 唱片主体
    draw.ellipse([cx-vinyl_r, cy-vinyl_r, cx+vinyl_r, cy+vinyl_r],
                fill=(18, 18, 18))
    draw.ellipse([cx-vinyl_r+2, cy-vinyl_r+2, cx+vinyl_r-2, cy+vinyl_r-2],
                outline=(58, 58, 58), width=2)

    # 凹槽（只画10条，间距大）
    for i in range(10):
        r = int(vinyl_r * 0.38 + i * vinyl_r * 0.055)
        if r > vinyl_r - 15:
            break
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(45, 45, 45), width=1)

    # 金色标签
    for idx in range(4):
        ratio = idx / 4
        lc = (
            int(240 - ratio*28),
            int(208 - ratio*118),
            int(112 - ratio*86)
        )
        lr = label_r - idx * 8
        draw.ellipse([cx-lr, cy-lr, cx+lr, cy+lr], fill=lc)

    # 封面图（正方形）
    cover_size = cover_r * 2
    if cover_path and os.path.exists(cover_path):
        try:
            cover = Image.open(cover_path).convert('RGB')
            cover = cover.resize((cover_size, cover_size), Image.LANCZOS)
            cover_x = cx - cover_r
            cover_y = cy - cover_r
            img.paste(cover, (cover_x, cover_y))
        except Exception as e:
            print(f"Cover error: {e}")

    # 中心孔
    hole_r = 8
    draw.ellipse([cx-hole_r, cy-hole_r, cx+hole_r, cy+hole_r], fill=(10,10,10))

    # 唱臂（贝塞尔曲线）
    import numpy as np
    pivot_x = cx + vinyl_r + 55
    pivot_y = 65
    needle_x = cx + int(vinyl_r * 0.52)
    needle_y = cy - int(vinyl_r * 0.25)
    
    ctrl_x = pivot_x - int(vinyl_r * 0.08)
    ctrl_y = pivot_y + int(height * 0.25)
    
    points = []
    steps = 20
    for t_i in range(steps+1):
        t = t_i / steps
        x = int((1-t)**2 * pivot_x + 2*(1-t)*t * ctrl_x + t**2 * needle_x)
        y = int((1-t)**2 * pivot_y + 2*(1-t)*t * ctrl_y + t**2 * needle_y)
        points.append((x, y))
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=(201,169,110), width=7)
    draw.ellipse([needle_x-5, needle_y-5, needle_x+5, needle_y+5],
                fill=(201,169,110))

    # 支点
    pr = 16
    draw.ellipse([pivot_x-pr, pivot_y-pr, pivot_x+pr, pivot_y+pr],
                fill=(212,168,75))
    draw.ellipse([pivot_x-pr, pivot_y-pr, pivot_x+pr, pivot_y+pr],
                outline=(201,169,110), width=2)
    draw.ellipse([pivot_x-4, pivot_y-4, pivot_x+4, pivot_y+4],
                fill=(40,40,40))

    # 歌曲名
    tx = cx  # 封面图中心X
    ty = cy + cover_r + 20  # 封面图下方20px

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
                font_large = ImageFont.truetype(fp, 36)
                font_small = ImageFont.truetype(fp, 14)
                break
        if font_small:
            draw.text((tx, ty), "LYRIC VIDEO", fill=(136,136,136), font=font_small, anchor="mt")
        if font_large:
            draw.text((tx, ty + 25), song_title, fill=(255,255,255), font=font_large, anchor="mt")
        else:
            draw.text((tx, ty), "LYRIC VIDEO", fill=(136,136,136))
            draw.text((tx, ty + 25), song_title, fill=(255,255,255))
    except Exception as e:
        print(f"Font error: {e}")

    img.save(output_path, 'PNG')
    print(f"Done: {output_path}")

if __name__ == "__main__":
    song_title = sys.argv[1] if len(sys.argv) > 1 else "AI 노래"
    cover_path = sys.argv[2] if len(sys.argv) > 2 else "work/cover.jpg"
    output = sys.argv[3] if len(sys.argv) > 3 else "work/vinyl_bg.png"
    generate_vinyl_image(song_title, cover_path, output)
