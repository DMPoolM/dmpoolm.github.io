#!/usr/bin/env python3
"""Check generated HTML, anchors, and local assets before publication."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
import struct

ROOT=Path(__file__).resolve().parents[1]/'public'
errors=[]

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set();self.links=[];self.h1=0;self.title=False;self.lang=False;self.meta={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids: errors.append(f'Duplicate ID: {a["id"]}')
            self.ids.add(a['id'])
        if tag=='html': self.lang=bool(a.get('lang'))
        if tag=='h1': self.h1+=1
        if tag=='title': self.title=True
        if tag=='meta': self.meta[a.get('property',a.get('name',''))]=a.get('content','')
        if tag=='img' and 'alt' not in a: errors.append('Image without alt text')
        for name in ['href','src']:
            if name in a: self.links.append(a[name])

documents={}
for file in ROOT.rglob('*.html'):
    parser=Document();parser.feed(file.read_text());documents[file]=parser
    if parser.h1!=1 or not parser.title or not parser.lang: errors.append(f'Page metadata/heading error: {file.relative_to(ROOT)}')
    if parser.meta.get('twitter:card')!='summary_large_image': errors.append(f'Missing social card: {file.relative_to(ROOT)}')
    image=urlsplit(parser.meta.get('og:image',''))
    if image.scheme!='https' or not (ROOT/image.path.lstrip('/')).is_file(): errors.append(f'Missing share image: {file.relative_to(ROOT)}')
for file,doc in documents.items():
    for link in doc.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc: continue
        path=unquote(parts.path)
        target=(ROOT/path.lstrip('/')) if path.startswith('/') else (file.parent/path if path else file)
        target=target.resolve()
        if target.is_dir(): target=target/'index.html'
        if not target.is_relative_to(ROOT.resolve()):
            errors.append(f'Link leaves public directory: {link}')
        elif not target.exists(): errors.append(f'{file.relative_to(ROOT)} -> missing {link}')
        elif parts.fragment and target in documents and unquote(parts.fragment) not in documents[target].ids:
            errors.append(f'{file.relative_to(ROOT)} -> missing anchor {link}')
pdf=ROOT/'assets'/'Fanze_Meng_Resume.pdf'
if not pdf.exists() or pdf.read_bytes()[:5]!=b'%PDF-': errors.append('Missing or invalid resume PDF')
png=ROOT/'assets'/'social-preview.png'
if not png.exists() or struct.unpack('>II',png.read_bytes()[16:24])!=(1200,630): errors.append('Share image must be 1200 × 630')
ico=ROOT/'favicon.ico'
if not ico.exists() or ico.read_bytes()[:4]!=b'\x00\x00\x01\x00': errors.append('Missing root favicon.ico')
css=(ROOT/'assets'/'site.css').read_text()
if any(int(x)<11 for x in re.findall(r'font-size:\s*(\d+)px',css)): errors.append('CSS contains font sizes below 11px')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(documents)} HTML pages; local links, social cards, favicon, CV, and auxiliary type sizes checked.')
