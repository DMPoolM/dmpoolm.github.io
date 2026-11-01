#!/usr/bin/env python3
"""Build the portfolio with Python's standard library; no package install needed."""
from pathlib import Path
from html import escape as esc
import json
import math
import random
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public'
DATA = json.loads((ROOT / 'content.json').read_text())
OUT.mkdir(exist_ok=True)
(OUT / 'assets').mkdir(exist_ok=True)
for asset in (ROOT / 'assets').iterdir():
    if asset.is_file():
        shutil.copyfile(asset, OUT / 'assets' / asset.name)

ARROW = '<span aria-hidden="true">↗</span>'


def tags(items):
    return '<ul class="tags" aria-label="Methods and tools">' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'


def layout(title, description, body, path='', prefix='./'):
    canonical = DATA['url'] + '/' + path
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#fafaf7">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description, quote=True)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title, quote=True)}">
  <meta property="og:description" content="{esc(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="header wrap">
  <a class="wordmark" href="{prefix}" aria-label="Fanze Meng, home"><span class="monogram" aria-hidden="true">fm<span>.</span></span><span>Fanze Meng</span></a>
  <nav aria-label="Main navigation">
    <a href="{prefix}#work">Work</a><a href="{prefix}#research">Research</a><a href="{prefix}#about">About</a>
    <a class="nav-contact" href="{prefix}#contact">Let’s talk {ARROW}</a>
  </nav>
</header>
{body}
<footer class="footer wrap"><a href="{prefix}" class="footer-name">Fanze Meng<span>Materials science × machine learning</span></a><p>© 2026 Fanze Meng · Updated {DATA['updated']}</p><a href="#main">Back to top ↑</a></footer>
</body></html>'''


def svg_start(title, width=640, height=360):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img"><title>{esc(title)}</title>'


def hero_svg():
    # A deliberately abstract lattice; not a particular chemical structure.
    nodes = []
    for z in range(3):
        for y in range(3):
            for x in range(3):
                nodes.append((x, y, z, 280 + (x-y)*66, 212 + (x+y)*30 - z*78))
    out = [svg_start('Abstract lattice illustration representing computational materials', 560, 520), '''<defs>
      <radialGradient id="atom"><stop stop-color="#e5eee6" offset="0"/><stop stop-color="#b1c7b6" offset=".55"/><stop stop-color="#789a89" offset="1"/></radialGradient>
      <radialGradient id="focus"><stop stop-color="#91c6b2" offset="0"/><stop stop-color="#297e68" offset=".65"/><stop stop-color="#165640" offset="1"/></radialGradient>
      <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#9cafa3" opacity=".33"/></pattern>
      </defs><rect width="560" height="520" fill="url(#dots)"/>
      <ellipse cx="280" cy="378" rx="192" ry="51" fill="#c8d7c9" opacity=".17"/>
      <ellipse cx="280" cy="270" rx="228" ry="177" fill="none" stroke="#b5c8b8" stroke-dasharray="4 7" opacity=".6"/>''']
    for x, y, z, px, py in nodes:
        for nx, ny, nz, qx, qy in nodes:
            if (nx-x, ny-y, nz-z) in [(1,0,0),(0,1,0),(0,0,1)]:
                out.append(f'<path d="M{px} {py}L{qx} {qy}" stroke="#8ba494" stroke-width="1.3" opacity=".65"/>')
    for x, y, z, px, py in sorted(nodes, key=lambda n: n[4]):
        active = (x+y+z) % 4 == 0
        out.append(f'<circle cx="{px}" cy="{py}" r="{13 if active else 9}" fill="url(#{"focus" if active else "atom"})" stroke="#f5faf2" stroke-width="1.5"/>')
    out.append('''<g fill="#335a4d" font-family="Arial,sans-serif" font-size="11" letter-spacing="1.7"><text x="35" y="52">STRUCTURE</text><text x="385" y="442">PROPERTY</text></g>
      <g stroke="#8ca797" fill="none"><path d="M104 61H151L185 100"/><path d="M376 433H341L320 395"/></g>
      <g fill="#53705f" font-family="monospace" font-size="10"><text x="34" y="483">01 / COMPUTATIONAL MATERIALS</text><text x="433" y="483">E(3)</text></g></svg>''')
    return ''.join(out)


def project_svg(slug):
    s = [svg_start('Conceptual workflow diagram; illustrative rather than experimental data')]
    s.append('<defs><pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="#b9cdbf" stroke-width=".6" opacity=".5"/></pattern></defs><rect width="640" height="360" fill="#edf2e9"/><rect width="640" height="360" fill="url(#grid)"/>')
    if slug == 'material-centre':
        s.append('''<rect x="68" y="53" width="504" height="251" rx="9" fill="#fffefa" stroke="#9caf9d"/>
        <path d="M68 87H572" stroke="#c8d3c6"/><circle cx="85" cy="71" r="3" fill="#1d6e56"/><circle cx="97" cy="71" r="3" fill="#b5c6b4"/><circle cx="109" cy="71" r="3" fill="#b5c6b4"/>
        <text x="132" y="75" fill="#577265" font-size="10" font-family="monospace">MATERIAL SEARCH / SCHEMATIC</text>
        <g font-family="Arial,sans-serif" fill="#284b3d"><text x="91" y="118" font-size="10">TARGET PROPERTIES</text><text x="281" y="118" font-size="10">SIMILAR CANDIDATES</text></g>
        <path d="M252 106V281" stroke="#d3ddcf"/>
        <g stroke="#cad6c7" stroke-width="4" stroke-linecap="round"><path d="M96 151H221M96 192H221M96 233H221"/></g>
        <g fill="#1f735a"><circle cx="179" cy="151" r="5"/><circle cx="137" cy="192" r="5"/><circle cx="198" cy="233" r="5"/></g>''')
        for i in range(4):
            y = 135 + i*36
            s.append(f'<rect x="278" y="{y}" width="267" height="27" rx="3" fill="{"#e2ede1" if i==0 else "#f2f5ed"}"/><text x="290" y="{y+18}" font-family="monospace" font-size="10" fill="#345848">0{i+1}</text><path d="M326 {y+14}H{491-i*23}" stroke="#90b5a0" stroke-width="5" stroke-linecap="round"/>')
    elif slug == 'stress-strain-prediction':
        rng=random.Random(12)
        s.append('<rect x="50" y="86" width="164" height="176" rx="4" fill="#d1dfc8" stroke="#aec2aa"/>')
        for i in range(35):
            x,y=rng.uniform(62,202),rng.uniform(98,250)
            s.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.randint(5,12)}" ry="{rng.randint(3,7)}" fill="#7b9c7f" opacity=".6" transform="rotate({rng.randint(0,180)} {x:.1f} {y:.1f})"/>')
        s.append('''<path d="M232 174H272M264 168L272 174L264 180M365 174H402M394 168L402 174L394 180" stroke="#336a53" fill="none" stroke-width="1.5"/>
        <rect x="286" y="134" width="64" height="80" rx="6" fill="#245f49"/>
        <g fill="#e2ebdf" font-family="monospace" font-size="11" text-anchor="middle"><text x="318" y="165">CNN</text><text x="318" y="185">+ ATT.</text></g>
        <path d="M425 99V250H597" fill="none" stroke="#92ad94"/>
        <path d="M426 246C443 148 456 139 486 132S540 119 582 107L582 141C535 150 519 149 490 158S449 174 426 246" fill="#a3c5a4" opacity=".45"/>
        <path d="M426 246C447 159 459 151 489 145S542 135 582 122" fill="none" stroke="#21684e" stroke-width="2.5"/>
        <g fill="#53705d" font-family="monospace" font-size="10" text-anchor="middle"><text x="132" y="293">MICROSTRUCTURE</text><text x="318" y="293">MODEL</text><text x="510" y="293">RESPONSE + UNCERTAINTY</text></g>''')
    elif slug == 'structure-screening':
        rng=random.Random(8)
        for cx,cy,col in [(152,117,'#2f7154'),(171,235,'#829d72'),(273,176,'#b0b765')]:
            for i in range(18):
                x,y=cx+rng.gauss(0,25),cy+rng.gauss(0,21)
                s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" opacity=".78"/>')
        s.append('<path d="M343 176H393M385 170L393 176L385 182" fill="none" stroke="#487057" stroke-width="1.5"/>')
        for cx,cy,col in [(470,110,'#2f7154'),(510,226,'#829d72'),(448,245,'#b0b765')]:
            s.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="{col}" opacity=".4"/><circle cx="{cx}" cy="{cy}" r="9" fill="{col}"/>')
        s.append('<g fill="#53705d" font-family="monospace" font-size="10" text-anchor="middle"><text x="200" y="310">STRUCTURE CANDIDATES</text><text x="476" y="310">GROUP + REVIEW</text></g>')
    else:
        for x,y,label,sub in [(58,124,'MANUALS','Retrieve'),(249,124,'LLM AGENT','Generate'),(440,124,'VALIDATION','Evaluate')]:
            s.append(f'<rect x="{x}" y="{y}" width="142" height="102" rx="5" fill="#fffefa" stroke="#9eb7a1"/><text x="{x+71}" y="{y+40}" text-anchor="middle" fill="#275c45" font-size="12" font-family="monospace">{label}</text><text x="{x+71}" y="{y+64}" text-anchor="middle" fill="#6c806b" font-size="11" font-family="Arial">{sub}</text>')
        s.append('<path d="M210 176H238M230 170L238 176L230 182M401 176H429M421 170L429 176L421 182" fill="none" stroke="#487057" stroke-width="1.5"/><path d="M511 239V275H320V239" stroke="#8ba38a" stroke-dasharray="4 5" fill="none"/>')
    s.append('</svg>')
    return ''.join(s)


(OUT/'assets'/'lattice.svg').write_text(hero_svg())
for project in DATA['projects']:
    (OUT/'assets'/f"{project['slug']}.svg").write_text(project_svg(project['slug']))

cards = []
for p in DATA['projects'][:3]:
    cards.append(f'''<article class="project-card">
      <a class="project-image" href="./projects/{p['slug']}/" aria-label="Read case study: {esc(p['title'])}"><img src="./assets/{p['slug']}.svg" alt="Conceptual diagram of {esc(p['title'], quote=True)}" width="640" height="360" loading="lazy"><span class="image-index">{p['number']} / SELECTED WORK</span><span class="image-link" aria-hidden="true">↗</span></a>
      <p class="eyebrow project-category">{esc(p['category'])}</p><h3><a href="./projects/{p['slug']}/">{esc(p['title'])}</a></h3><p class="card-summary">{esc(p['summary'])}</p>
      {tags(p['tags'][:3])}<a class="text-link" href="./projects/{p['slug']}/">Read case study <span aria-hidden="true">↗</span></a>
    </article>''')

education=''.join(f'''<li><p class="education-date">{esc(e['date'])}</p><h3>{esc(e['school'])}</h3><p>{esc(e['degree'])}</p><p class="muted">{esc(e['detail'])}</p></li>''' for e in DATA['education'])
publications=''.join(f'''<li><span class="publication-year">{p['year']}</span><div><h3><a href="https://doi.org/{p['doi']}">{esc(p['title'])} {ARROW}</a></h3><p>{esc(p['authors'])}</p><p class="muted">{esc(p['venue'])}</p></div></li>''' for p in DATA['publications'])
body=f'''
<main id="main">
<section class="hero wrap" aria-labelledby="intro-title">
  <div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> Computational materials · Japan</p>
    <h1 id="intro-title">Machine learning<br>for <em>materials</em><br>and engineering.</h1>
    <p class="hero-intro">{esc(DATA['intro'])}</p>
    <div class="actions"><a class="button" href="#work">Explore my work <span aria-hidden="true">↓</span></a><a class="button button-light" href="./assets/Fanze_Meng_Resume.pdf" download>Download résumé <span class="pdf-label">PDF ↗</span></a></div>
    <div class="hero-social"><a href="{DATA['github']}">GitHub {ARROW}</a><a href="{DATA['linkedin']}">LinkedIn {ARROW}</a><a href="mailto:{DATA['email']}">Email {ARROW}</a></div>
  </div>
  <figure class="hero-figure"><img src="./assets/lattice.svg" alt="Abstract lattice of connected atoms, representing computational materials" width="560" height="520"><figcaption><span>From structure to understanding.</span><span>Illustrative lattice</span></figcaption></figure>
</section>
<div class="affiliations wrap"><p>Research &amp;<br>engineering experience</p><ul><li>Science Tokyo</li><li>Volvo Cars</li><li>Chalmers</li><li>Tohoku University</li></ul></div>

<section class="section wrap" id="work" aria-labelledby="work-title">
  <div class="section-heading"><div><p class="eyebrow">01 / Selected work</p><h2 id="work-title">Ideas, models, and useful tools.</h2></div><p>Selected work across materials informatics,<br>scientific computing, and industrial R&amp;D.</p></div>
  <div class="project-grid">{''.join(cards)}</div>
  <a class="additional-project" href="./projects/robot-code-agent/"><span class="mini-number">04</span><span><span class="eyebrow">MSc thesis · Chalmers × Volvo Cars</span><strong>An LLM agent for industrial robot code</strong></span><span class="additional-project-end">Explore project {ARROW}</span></a>
</section>

<section class="research-band" id="research" aria-labelledby="research-title"><div class="wrap research-grid">
  <div><p class="eyebrow">02 / Current research</p><h2 id="research-title">From pair distributions<br>to atomic structures.</h2><span class="research-status"><span class="status-dot"></span> In progress · Since October 2026</span></div>
  <div><p class="research-intro">I’m developing physics-aware generative models to reconstruct 3D atomic structures from pair distribution functions, with solid electrolytes for batteries as the target application.</p><p>The planned approach uses conditional flow matching and physical constraints, with validation through machine-learned interatomic potentials and molecular dynamics. This is ongoing MSc research; completed benchmark results are not yet presented here.</p><p class="lab-note">Tateyama–Ando Lab<br>Institute of Science Tokyo</p></div>
</div></section>

<section class="section wrap publications" aria-labelledby="publications-title"><div class="section-heading"><div><p class="eyebrow">03 / Publications</p><h2 id="publications-title">Earlier work in materials &amp; chemistry.</h2></div><p>Co-authored publications.</p></div><ol class="publication-list">{publications}</ol></section>

<section class="section wrap about-grid" id="about" aria-labelledby="about-title"><div><p class="eyebrow">04 / A little background</p><h2 id="about-title">Materials foundations.<br>Computational perspective.</h2><p class="about-intro">My background spans materials science in London, engineering mathematics in Gothenburg, and computational materials research in Japan.</p><p>I’m interested in models that respect physical behaviour, uncertainty that helps guide decisions, and research software that people can use. Alongside modelling, I have hands-on experience in thin-film fabrication, battery materials, and materials characterisation.</p><a class="text-link" href="./assets/Fanze_Meng_Resume.pdf">View my résumé (PDF) {ARROW}</a></div><ol class="education-list">{education}</ol></section>

<section class="contact-band" id="contact" aria-labelledby="contact-title"><div class="wrap contact-grid"><div><p class="eyebrow">05 / Get in touch</p><h2 id="contact-title">Let’s connect.</h2><p>For research conversations, collaborations,<br>or opportunities in materials and machine learning.</p></div><div class="contact-links"><a class="email-link" href="mailto:{DATA['email']}">{DATA['email']} {ARROW}</a><div><a href="{DATA['github']}">GitHub {ARROW}</a><a href="{DATA['linkedin']}">LinkedIn {ARROW}</a></div><span>Based in Japan · Chinese / English / Learning Japanese</span></div></div></section>
</main>'''
(OUT/'index.html').write_text(layout('Fanze Meng — Materials Science & Machine Learning', 'Computational materials MSc student at Institute of Science Tokyo. Selected work in materials machine learning, scientific software, and generative AI.', body))

for i,p in enumerate(DATA['projects']):
    next_p=DATA['projects'][(i+1)%len(DATA['projects'])]
    methods=''.join(f'<li>{esc(m)}</li>' for m in p['methods'])
    detail=f'''<main id="main" class="case-main wrap"><a class="back-link" href="../../#work">← Selected work</a>
    <header class="case-header"><p class="eyebrow">Case study {p['number']} / {esc(p['category'])}</p><h1>{esc(p['title'])}</h1><p class="case-subtitle">{esc(p['subtitle'])}</p>
    <dl class="case-meta"><div><dt>Context</dt><dd>{esc(p['context'])}</dd></div><div><dt>Period</dt><dd>{esc(p['date'])}</dd></div></dl>{tags(p['tags'])}</header>
    <figure class="case-figure"><img src="../../assets/{p['slug']}.svg" width="640" height="360" alt="Conceptual workflow diagram"><figcaption>{esc(p['figure_caption'])}</figcaption></figure>
    <div class="case-grid"><aside class="case-highlight"><p class="eyebrow">Project outcome</p><p>{esc(p['result'])}</p></aside>
    <div class="case-copy"><section><h2>The problem</h2><p>{esc(p['problem'])}</p></section><section><h2>My contribution</h2><p>{esc(p['contribution'])}</p></section><section><h2>Methods &amp; implementation</h2><ul>{methods}</ul></section><section><h2>Outcome &amp; scope</h2><p>{esc(p['outcome'])}</p></section></div></div>
    <div class="case-next"><a href="../../#work">← All selected work</a><a href="../{next_p['slug']}/">Next: {esc(next_p['title'])} →</a></div></main>'''
    folder=OUT/'projects'/p['slug']
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'index.html').write_text(layout(p['title']+' — Fanze Meng',p['summary'],detail,f"projects/{p['slug']}/",'../../'))

# Absolute root paths keep the error page usable for deeply nested unknown URLs.
error='''<main id="main" class="wrap error-page"><p class="eyebrow">404 / Page not found</p><h1>This page isn’t here.</h1><p>You can return to the portfolio to explore my work.</p><a class="button" href="/">Back to the portfolio →</a></main>'''
(OUT/'404.html').write_text(layout('Page not found — Fanze Meng','Return to Fanze Meng’s portfolio.',error,'404.html','/').replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"'))
(OUT/'.nojekyll').touch()
(OUT/'robots.txt').write_text(f"User-agent: *\nAllow: /\nSitemap: {DATA['url']}/sitemap.xml\n")
urls=['']+[f"projects/{p['slug']}/" for p in DATA['projects']]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{DATA["url"]}/{u}</loc></url>' for u in urls)+'</urlset>')
print(f"Built {len(urls)} pages and a 404 page in {OUT}")
