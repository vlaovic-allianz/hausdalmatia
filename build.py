#!/usr/bin/env python3
"""Erzeugt die Sprachversionen der Website aus der deutschen Quelle.

    python3 build.py

Quelle:   index.html (Deutsch) – Texte mit data-i18n, Übersetzungen im Objekt I18N im Skript.
Ergebnis: en/index.html, pl/index.html, hr/index.html (fertig übersetzt, für Google lesbar).
Nach jeder Änderung an index.html bitte erneut ausführen. Voraussetzung: Python 3 mit bs4, Node.js.
"""
import json, re, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SITE = 'https://hausdalmatia.com/'
LOCALES = {'de': 'de_DE', 'en': 'en_GB', 'pl': 'pl_PL', 'hr': 'hr_HR'}
ASSET = re.compile(r'^(bilder/|fonts/|impressum\.html|datenschutz\.html|legal\.css)')


def load_i18n(src):
    """Liest das Objekt I18N aus dem Skript (mit Node, damit die JS-Syntax exakt geprüft wird)."""
    m = re.search(r'\nvar I18N = (\{.*?\n\});\n', src, re.S)
    if not m:
        sys.exit('I18N-Objekt nicht gefunden')
    out = subprocess.run(['node', '-e', 'process.stdout.write(JSON.stringify(' + m.group(1) + '))'],
                         capture_output=True, text=True)
    if out.returncode:
        sys.exit('Fehler im Übersetzungsobjekt:\n' + out.stderr)
    return json.loads(out.stdout)


def relink(soup):
    """Pfade auf Bilder, Schriften und Unterseiten eine Ebene höher legen (../)."""
    for el in soup.find_all(True):
        for attr in ('src', 'href', 'data-src', 'data-full', 'srcset', 'data-srcset', 'imagesrcset'):
            v = el.get(attr)
            if not v:
                continue
            if 'srcset' in attr:
                el[attr] = ', '.join(('../' + p.strip()) if ASSET.match(p.strip()) else p.strip() for p in v.split(','))
            elif ASSET.match(v):
                el[attr] = '../' + v
    for st in soup.find_all('style'):
        st.string = st.string.replace('url(fonts/', 'url(../fonts/')


def faq_ld(soup):
    """FAQPage-Daten aus den sichtbaren Fragen erzeugen (Wortlaut identisch mit der Seite)."""
    items = [{'@type': 'Question', 'name': d.summary.get_text(' ', strip=True),
              'acceptedAnswer': {'@type': 'Answer', 'text': d.select_one('.ans').get_text(' ', strip=True)}}
             for d in soup.select('.faq-list details')]
    return json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': items}, ensure_ascii=False)


def set_faq(soup):
    soup.find('script', id='ld-faq').string = faq_ld(soup)


def build(lang, src, d):
    soup = BeautifulSoup(src, 'html.parser')
    soup.html['lang'] = lang
    soup.title.string = d['__title']
    soup.find('meta', attrs={'name': 'description'})['content'] = d['__desc']
    url = SITE + lang + '/'
    soup.find('link', rel='canonical')['href'] = url
    soup.find('meta', property='og:url')['content'] = url
    soup.find('meta', property='og:title')['content'] = d['__title']
    soup.find('meta', property='og:description')['content'] = d['__desc']
    soup.find('meta', property='og:locale')['content'] = LOCALES[lang]
    for m in soup.find_all('meta', property='og:locale:alternate'):
        m.decompose()
    og = soup.find('meta', property='og:locale')
    for l, loc in LOCALES.items():
        if l != lang:
            t = soup.new_tag('meta', property='og:locale:alternate', content=loc)
            og.insert_after(t)
    for el in soup.select('[data-i18n]'):
        k = el['data-i18n']
        if k in d:
            el.clear()
            el.append(BeautifulSoup(d[k], 'html.parser'))
    for el in soup.select('[data-i18n-alt]'):
        if el['data-i18n-alt'] in d:
            el['alt'] = d[el['data-i18n-alt']]
    for el in soup.select('[data-i18n-ph]'):
        if el['data-i18n-ph'] in d:
            el['placeholder'] = d[el['data-i18n-ph']]
    # Strukturierte Daten in der jeweiligen Sprache
    for sc in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(sc.string)
        except (TypeError, ValueError):
            continue
        if data.get('@type') == 'LodgingBusiness':
            data.update(url=url, inLanguage=lang, description=d['__desc'])
            sc.string = json.dumps(data, ensure_ascii=False, indent=2)
    set_faq(soup)
    relink(soup)
    for a in soup.select('.lang-switch a'):
        l = a['data-lang']
        a['href'] = '../' if l == 'de' else ('./' if l == lang else '../' + l + '/')
        a['class'] = ['active'] if l == lang else []
        if l == lang:
            a['aria-current'] = 'page'
        elif a.has_attr('aria-current'):
            del a['aria-current']
    return str(soup)


def main():
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    i18n = load_i18n(src)
    # FAQ-Daten der deutschen Seite aktualisieren (nur der Inhalt dieses einen Skript-Blocks)
    m = re.search(r'(<script type="application/ld\+json" id="ld-faq">)(.*?)(</script>)', src, re.S)
    if m:
        new = faq_ld(BeautifulSoup(src, 'html.parser'))
        if m.group(2) != new:
            src = src[:m.start(2)] + new + src[m.end(2):]
            (ROOT / 'index.html').write_text(src, encoding='utf-8')
            print('aktualisiert: FAQ-Daten in index.html')
    for lang in [l for l in LOCALES if l != 'de']:
        if lang not in i18n:
            continue
        missing = sorted({el['data-i18n'] for el in BeautifulSoup(src, 'html.parser').select('[data-i18n]')} - set(i18n[lang]))
        if missing:
            print(f'Hinweis {lang}: fehlende Übersetzungen {missing}')
        out = ROOT / lang / 'index.html'
        out.parent.mkdir(exist_ok=True)
        out.write_text(build(lang, src, i18n[lang]), encoding='utf-8')
        print('geschrieben:', out.relative_to(ROOT))


if __name__ == '__main__':
    main()
