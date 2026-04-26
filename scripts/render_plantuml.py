#!/usr/bin/env python3
"""
Renderiza archivos .puml en docs/diagrams a PNG y SVG usando el servidor público de PlantUML.
Realiza una petición GET con la codificación requerida por PlantUML; si falla, hace POST como fallback.
Uso: python3 scripts/render_plantuml.py
"""
import os
import sys
import zlib
from urllib import request, error

DIAGRAM_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'diagrams'))
FORMATS = ['png', 'svg']
SERVER = 'https://www.plantuml.com/plantuml'

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def encode_6bit(b):
    return ALPHABET[b]


def append3bytes(b1, b2, b3):
    c1 = (b1 >> 2) & 0x3F
    c2 = ((b1 & 0x3) << 4) | ((b2 >> 4) & 0xF)
    c3 = ((b2 & 0xF) << 2) | ((b3 >> 6) & 0x3)
    c4 = b3 & 0x3F
    return encode_6bit(c1) + encode_6bit(c2) + encode_6bit(c3) + encode_6bit(c4)


def encode64(data: bytes) -> str:
    res = []
    i = 0
    while i < len(data):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        res.append(append3bytes(b1, b2, b3))
        i += 3
    return ''.join(res)


def plantuml_encode(text: str) -> str:
    data = text.encode('utf-8')
    compressed = zlib.compress(data)
    # strip zlib header and adler32 checksum
    compressed = compressed[2:-4]
    return encode64(compressed)


def render_get(diagram_text: str, fmt: str) -> bytes:
    code = plantuml_encode(diagram_text)
    url = f"{SERVER}/{fmt}/{code}"
    req = request.Request(url, headers={'User-Agent': 'render-script'})
    with request.urlopen(req, timeout=60) as resp:
        return resp.read()


def render_post(diagram_text: str, fmt: str) -> bytes:
    url = f"{SERVER}/{fmt}/"
    req = request.Request(url, data=diagram_text.encode('utf-8'), headers={'Content-Type': 'text/plain'})
    with request.urlopen(req, timeout=60) as resp:
        return resp.read()


def render_file(path: str, fmt: str):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    try:
        out = render_get(text, fmt)
    except Exception:
        # intento fallback por POST
        out = render_post(text, fmt)
    out_path = os.path.splitext(path)[0] + '.' + fmt
    with open(out_path, 'wb') as of:
        of.write(out)
    print(f'Wrote: {out_path}')


def main():
    if not os.path.isdir(DIAGRAM_DIR):
        print(f'Directory not found: {DIAGRAM_DIR}', file=sys.stderr)
        sys.exit(1)
    files = [f for f in os.listdir(DIAGRAM_DIR) if f.endswith('.puml')]
    if not files:
        print('No .puml files found in', DIAGRAM_DIR, file=sys.stderr)
        sys.exit(1)
    for f in files:
        p = os.path.join(DIAGRAM_DIR, f)
        for fmt in FORMATS:
            try:
                render_file(p, fmt)
            except error.HTTPError as e:
                print(f'HTTP error rendering {p} -> {fmt}: {e}', file=sys.stderr)
            except Exception as e:
                print(f'Error rendering {p} -> {fmt}: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
