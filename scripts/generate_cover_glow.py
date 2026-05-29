import numpy as np
from PIL import Image

SIZE = 328
MAX_GLOW_DIST = 16  # glow fades off 16px inward from each edge

y_idx, x_idx = np.ogrid[:SIZE, :SIZE]
dist = np.minimum(
    np.minimum(x_idx, SIZE - 1 - x_idx),
    np.minimum(y_idx, SIZE - 1 - y_idx)
)

# Exponential decay: bright at border, transparent toward center
glow = np.where(dist <= MAX_GLOW_DIST, np.exp(-dist / 4.5), 0.0)

img_array = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
img_array[:, :, 0] = 74    # R  (#4af0ff)
img_array[:, :, 1] = 240   # G
img_array[:, :, 2] = 255   # B
img_array[:, :, 3] = (glow * 210).astype(np.uint8)  # A: max 210/255

Image.fromarray(img_array, 'RGBA').save('work/cover_glow.png')
print(f'cover_glow.png generated: {SIZE}x{SIZE}')
