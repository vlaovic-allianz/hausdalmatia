"""Haus-Dalmatia-Look: einheitliche Bildbearbeitung für alle Fotos der Website.

    python3 werkzeuge/look.py            # alle Bilder neu erzeugen
    python3 werkzeuge/look.py vorschau   # nur Vergleichsbild (vorher | nachher) in bilder/look-vorschau.jpg

Warmes Adria-Licht, sanfte S-Kurve, Vibrance statt Sättigung (kräftige Farben wie das Pool-Türkis
werden nicht übersteuert), kühle Schatten / warme Lichter, feine Detailschärfe.
Quelle: bilder/hd/ (aufgewertete Master) bzw. Original-Fotos; Ergebnis: bilder/hd-look/ und bilder/web/.
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
B = os.path.join(ROOT, 'bilder')


def look(im, strength=1.6):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0
    s = strength
    # 1. Weißabgleich: einen Hauch wärmer
    a[..., 0] *= 1 + .018 * s; a[..., 2] *= 1 - .028 * s
    a = np.clip(a, 0, 1)
    # 2. Tonkurve: Schwarz minimal angehoben, sanfte S-Kurve, Lichter weich abgerundet
    sm = a * a * (3 - 2 * a)
    a = a + (sm - a) * .20 * s
    a = .015 * s + a * (1 - .015 * s)
    a = 1 - (1 - a) ** (1 + .06 * s)
    # 3. Vibrance: blasse Farben kräftiger, sehr kräftige Farben unverändert bzw. leicht zurück
    mx, mn = a.max(-1, keepdims=True), a.min(-1, keepdims=True)
    sat = mx - mn
    lum = (a[..., :1] * .2126 + a[..., 1:2] * .7152 + a[..., 2:3] * .0722)
    f = 1 + s * (.22 * (1 - sat) ** 2 - .10 * sat ** 2)
    a = lum + (a - lum) * f
    # 4. Farbtiefe: Schatten leicht kühl (Meer), Lichter leicht warm (Abendsonne)
    lum = np.clip(lum, 0, 1)
    a += s * (np.array([-.010, .004, .016]) * (1 - lum) ** 2 + np.array([.016, .007, -.012]) * lum ** 2)
    out = Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
    # 5. Feine Detailschärfe (Klarheit)
    return out.filter(ImageFilter.UnsharpMask(radius=1.8, percent=45, threshold=4))  # Schwelle schont Flächen (Himmel, Wasser)


# Name auf der Website -> (Quelle, Breiten)
DIRECT = {
    'hero-meerblick': ('hd/hero-meerblick.jpg', [960, 1600, 2200]),
    'apt-more': ('hd/apt-more.jpg', [800, 1400, 2000]),
    'apt-maslina': ('hd/apt-maslina.jpg', [800, 1400, 1900]),
    'apt-riva': ('hd/apt-riva.jpg', [800, 1400, 1900]),
    'apt-zora': ('hd/apt-zora.jpg', [800, 1400, 1900]),
    'pool': ('hd/pool.jpg', [800, 1400, 1900]),
    'pool-abend': ('hd/pool-abend.jpg', [800, 1400, 1900]),
    'spielplatz': ('hd/spielplatz.jpg', [800, 1400, 1900]),
    'strand-bibinje': ('hd/strand-bibinje.jpg', [800, 1400, 1900]),
    'wassersport': ('hd/wassersport.jpg', [800, 1400, 1900]),
    'zadar': ('1920px-Sunset_in_Zadar_3.jpg', [800, 1400, 1900]),
    'krka': ('1920px-Krka_Skradinski-buk.jpg', [800, 1400, 1900]),
    'kornati': ('kornati.jpg', [800, 1400, 1900]),
}
# Ausschnitte fürs Titelbild (unbearbeitete Vorlagen in bilder/hd/*-ausschnitt.webp)
CROPS = {'hero-pool': [960, 1600], 'hero-abend': [960, 1600], 'hero-strand': [960, 1600]}
# Für den Titelfilm: bearbeitete Master in voller Größe
FILM = ['hero-meerblick', 'apt-more', 'pool', 'pool-abend', 'zadar']


# Sehr detailreiche Motive (Kiesel, Wasserfälle) etwas stärker komprimieren – sonst werden sie unnötig groß
FEIN = ('strand-bibinje', 'hero-strand', 'krka', 'wassersport')


def save(im, w, path):
    h = round(w * im.height / im.width)
    r = im if im.width == w else im.resize((w, h), Image.LANCZOS)
    q = 82 if w <= 1000 else 78
    if os.path.basename(path).startswith(FEIN): q -= 8
    r.save(path, 'WEBP', quality=q, method=6)
    return r.size


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'vorschau':
        tiles = []
        for n in ('hero-meerblick', 'pool', 'apt-more', 'strand-bibinje', 'apt-riva', 'zadar'):
            src = Image.open(os.path.join(B, DIRECT[n][0])).convert('RGB'); src.thumbnail((700, 700))
            tiles.append((src, look(src)))
        W = 1400; y = 0; sheet = Image.new('RGB', (W, sum(t[0].height for t in tiles) + 10 * len(tiles)), 'white')
        for a, b in tiles:
            sheet.paste(a, (0, y)); sheet.paste(b, (700, y)); y += a.height + 10
        sheet.save(os.path.join(B, 'look-vorschau.jpg'), quality=88); print('bilder/look-vorschau.jpg'); return
    os.makedirs(os.path.join(B, 'hd-look'), exist_ok=True)
    for n, (src, widths) in DIRECT.items():
        m = look(Image.open(os.path.join(B, src)))
        if n in FILM:
            m.save(os.path.join(B, 'hd-look', n + '.jpg'), quality=95)
        for w in widths:
            print(n, w, save(m, min(w, m.width), os.path.join(B, 'web', f'{n}-{w}.webp')))
    for n, widths in CROPS.items():
        m = look(Image.open(os.path.join(B, 'hd', n + '-ausschnitt.webp')))
        for w in widths:
            print(n, w, save(m, w, os.path.join(B, 'web', f'{n}-{w}.webp')))


if __name__ == '__main__':
    main()
