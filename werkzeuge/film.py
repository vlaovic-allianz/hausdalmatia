"""Titelfilm aus den aufgewerteten Fotos: ruhige Kamerafahrten mit Überblendungen, nahtlose Schleife.
python3 werkzeuge/film.py quer|hoch|quer4k [webm]  -> schreibt MP4 (H.264) bzw. WebM (VP9) nach bilder/film/"""
import math, subprocess, sys, os
from PIL import Image, ImageEnhance

HD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bilder', 'hd') + '/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bilder', 'film') + '/'
os.makedirs(OUT, exist_ok=True)
mode = sys.argv[1]
W, H, CRF = {'quer': (1920, 1080, 25), 'hoch': (720, 1280, 25), 'quer4k': (3840, 2160, 18)}[mode]
FPS, DUR, FADE = 25, 6.5, 1.3

# (Datei, Start (cx, cy, Breite als Anteil der Bildbreite), Ende (...)) – quer 16:9 bzw. hoch 9:16
SHOTS = {
 'quer': [('hero-meerblick', (.50, .50, 1.0), (.47, .41, .80)),
          ('pool', (.50, .30, 1.0), (.50, .66, 1.0)),
          ('strand-bibinje', (.45, .34, .90), (.55, .63, .90)),
          ('pool-abend', (.56, .55, .80), (.50, .50, 1.0))],
 'hoch': [('hero-meerblick', (.40, .50, .375), (.56, .52, .34)),
          ('pool', (.50, .50, .669), (.45, .56, .58)),
          ('strand-bibinje', (.40, .50, .5625), (.62, .50, .5625)),
          ('pool-abend', (.70, .50, .347), (.45, .50, .347))],
}
SHOTS['quer4k'] = SHOTS['quer']
shots = SHOTS[mode]

# Quellen laden, leicht veredeln (etwas Kontrast und Wärme, einheitlicher Look)
src = []
for name, a, b in shots:
    im = Image.open(HD + name + '.jpg').convert('RGB')
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Color(im).enhance(1.05)
    r, g, bl = im.split()
    r = r.point(lambda v: min(255, v * 1.015)); bl = bl.point(lambda v: v * .985)
    im = Image.merge('RGB', (r, g, bl))
    # Vorverkleinern, damit beim Ausschnitt kein Flimmern (Aliasing) entsteht
    minw = min(a[2], b[2]) * im.width
    f = min(1.0, W * 1.15 / minw)
    if f < 1: im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    src.append(im)

def ease(t): return .5 - .5 * math.cos(math.pi * max(0, min(1, t)))

def frame(i, u):
    im = src[i]; (cx0, cy0, w0), (cx1, cy1, w1) = shots[i][1], shots[i][2]
    e = ease(u / DUR)
    cx, cy, w = cx0 + (cx1 - cx0) * e, cy0 + (cy1 - cy0) * e, w0 + (w1 - w0) * e
    bw = w * im.width; bh = bw * H / W
    x0 = cx * im.width - bw / 2; y0 = cy * im.height - bh / 2
    x0 = max(0, min(im.width - bw, x0)); y0 = max(0, min(im.height - bh, y0))
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + bw, y0 + bh), Image.BICUBIC)

n = len(shots); step = DUR - FADE; T = n * step
WEBM = len(sys.argv) > 2 and sys.argv[2] == 'webm'
FILE = OUT + f'titelfilm-{mode}.' + ('webm' if WEBM else 'mp4')
cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
cmd += (['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', str(CRF + 9), '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2', '-pix_fmt', 'yuv420p', '-an', FILE] if WEBM else
        ['-c:v', 'libx264', '-preset', 'slow', '-crf', str(CRF), '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', '-an', FILE])
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for k in range(round(T * FPS)):
    t = k / FPS
    i = int(t // step); u = t - i * step
    img = frame(i, u)
    if u < FADE:  # vorherige Einstellung blendet aus; am Anfang ist das die letzte = nahtlose Schleife
        prev = frame((i - 1) % n, u + step)
        img = Image.blend(prev, img, ease(u / FADE))
    p.stdin.write(img.tobytes())
p.stdin.close(); p.wait()
print(FILE, W, H, round(T, 1), 's', os.path.getsize(FILE) // 1024, 'KB')
