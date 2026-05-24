import sys
import subprocess

svg_path = sys.argv[1]
png_path = sys.argv[2]

subprocess.run([
    'inkscape', '--export-type=png',
    f'--export-filename={png_path}',
    '--export-width=1280',
    '--export-height=720',
    svg_path
], check=True)
print(f"PNG generated: {png_path}")
