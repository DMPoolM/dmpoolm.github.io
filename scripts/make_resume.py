#!/usr/bin/env python3
"""Create the general public CV in the website's Georgia / Arial typography."""
from pathlib import Path
from html import escape
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'content.json').read_text())
FONTS = Path('/System/Library/Fonts/Supplemental')
for name,file in [('Body','Arial.ttf'),('BodyBold','Arial Bold.ttf'),('BodyItalic','Arial Italic.ttf'),('Display','Georgia.ttf'),('DisplayItalic','Georgia Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
INK, GREEN, MUTED = [colors.HexColor(c) for c in ['#20352c','#215f48','#526458']]
styles = {
 'name':ParagraphStyle('name',fontName='Display',fontSize=31,leading=36,textColor=INK,spaceAfter=8),
 'subtitle':ParagraphStyle('subtitle',fontName='DisplayItalic',fontSize=13,leading=18,textColor=GREEN,spaceAfter=7),
 'contact':ParagraphStyle('contact',fontName='Body',fontSize=9.5,leading=14,textColor=MUTED),
 'intro':ParagraphStyle('intro',fontName='Body',fontSize=10.2,leading=14.4,textColor=INK,spaceAfter=8),
 'section':ParagraphStyle('section',fontName='Display',fontSize=17,leading=22,textColor=GREEN,spaceBefore=16,spaceAfter=9,keepWithNext=True),
 'heading':ParagraphStyle('heading',fontName='BodyBold',fontSize=10.2,leading=14,textColor=INK),
 'date':ParagraphStyle('date',fontName='Body',fontSize=9.5,leading=14,textColor=MUTED,alignment=2),
 'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=14,textColor=INK,spaceAfter=6),
 'meta':ParagraphStyle('meta',fontName='Body',fontSize=9.5,leading=13.5,textColor=MUTED,spaceAfter=6),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=10,leading=14,textColor=INK,leftIndent=11,firstLineIndent=-11,spaceAfter=5),
}
story=[]
def p(text,style='body'): return Paragraph(text,styles[style])
def section(text): story.append(p(text,'section'))
def row(label,date):
    t=Table([[p(label,'heading'),p(date,'date')]],colWidths=[341,154],hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(t)
def bullet(text): story.append(p('• '+text,'bullet'))

story.append(p('Fanze Meng','name'))
story.append(p('Materials science, engineering mathematics, and computing','subtitle'))
story.append(p('Japan  |  <link href="mailto:'+data['email']+'">'+data['email']+'</link>','contact'))
story.append(p('<link href="'+data['url']+'">dmpoolm.github.io</link>  |  <link href="'+data['github']+'">GitHub</link>  |  <link href="'+data['linkedin']+'">LinkedIn</link>','contact'))
story.append(Spacer(1,13))
story.append(p('MSc student in computational materials at Institute of Science Tokyo, with degrees in materials science and engineering mathematics. Experience spans generative atomistic modelling, materials machine learning, experimental materials research, and software for industrial R&amp;D.','intro'))

section('Education')
for e in data['education']:
    row(escape(e['school']),e['date'].replace('–','-'))
    story.append(p(escape(e['degree'].replace('·','|').replace('–','-'))))
story.append(p('Completed the Chalmers MSc in June 2026; began a second MSc focused on computational materials at Science Tokyo in October 2026.','meta'))

section('Engineering experience')
row('Volvo Cars | Materials &amp; AI internship','Feb 2025 - Jan 2026')
bullet('Developed and deployed Material Centre, an interactive materials-search application using Streamlit, Plotly, PCA, and distance metrics; containerised with Docker for internal user testing.')
bullet('Built CNN-Transformer models for stress-strain prediction from microstructure images of 90 representative volume elements; validation R<super>2</super> = 0.89, with Monte Carlo-dropout uncertainty estimates.')
bullet('Added a physics-informed variant with elastic-modulus, smoothness, and boundary-condition losses.')
story.append(Spacer(1,6))
row('EDF, China R&amp;D Center | R&amp;D Assistant','Jun 2024 - Sep 2024')
story.append(p('Supported research on additive manufacturing for power-plant repair, analysing application cases and co-writing a technology roadmap. Researched HPC requirements for manufacturing, safety, data analysis, and materials R&amp;D.'))

section('Master\u2019s thesis')
row('Chalmers × Volvo Cars | Generative AI for robotics','Oct 2025 - Jun 2026')
bullet('Co-developed a proof-of-concept LLM agent using the OpenAI GPT API and retrieval over ABB manuals to generate RAPID robot code.')
bullet('Implemented an HPC-based code-validation framework; benchmarked the workflow on approximately 50 manufacturing tasks and analysed scalability.')

story.append(PageBreak())
section('Current research')
row('Institute of Science Tokyo | Tateyama-Ando Lab','Oct 2026 - present')
story.append(p('Physics-aware generative models for reconstructing periodic 3D atomic structures from pair distribution functions, targeting solid electrolytes for batteries.'))
bullet('Implemented structure-to-distribution preprocessing, grouped dataset splits, and data-quality diagnostics.')
bullet('Implemented conditional flow-matching training and sampling, a diffusion baseline, and structural evaluation with short MLIP relaxation.')
story.append(p('Current focus: data coverage, local bonding, and comparison with simpler baselines.','meta'))

section('Research and experimental background')
row('Tohoku University | COLABS research exchange','Sep 2024 - Feb 2025')
bullet('Built a graph-similarity clustering pipeline for 3D electron diffraction candidates, reducing the number requiring manual verification by 97.2% on average across 7 datasets (2,127 structures).')
bullet('Replicated a catalyst-screening study with pretrained FAIR-Chem GNN models, including adsorbate-slab generation, ML relaxations, and comparison with literature adsorption energies.')
story.append(Spacer(1,5))
row('Undergraduate laboratory research','2021 - 2023')
story.append(p('Worked on thin-film fabrication for flexible displays and on aqueous flexible zinc-ion battery materials. Experience includes electrodeposition, electrode-separator fabrication, IR spectroscopy, XRD, SEM, and electrochemical testing.'))

section('Tools and interests')
story.append(p('<b>Programming and ML:</b> Python, C, MATLAB/Simulink, Julia, SQL; PyTorch, TensorFlow, scikit-learn, XGBoost; generative models, uncertainty estimation, LLM agents, and RAG.'))
story.append(p('<b>Scientific software:</b> FAIR-Chem, ASE, RDKit; Linux, Git, Docker, Azure, Streamlit, Plotly; parallel computing, image analysis, and control systems.'))
story.append(p('<b>Languages:</b> Chinese (native), English (fluent; IELTS 7.5), Japanese (actively studying). <b>Personal interests:</b> hiking, cycling, driving.'))

section('Publications')
story.append(p('Collaborative papers from undergraduate study.','meta'))
for pub in data['publications']:
    story.append(p(escape(pub['authors'])+'. '+escape(pub['title'])+'. <i>'+escape(pub['venue'])+'</i> ('+pub['year']+'). <link href="https://doi.org/'+pub['doi']+'">doi:'+pub['doi']+'</link>.'))

def page_frame(canvas,doc):
    w,h=A4
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#215f48'))
    canvas.rect(0,h-10,w,10,fill=1,stroke=0)
    canvas.setStrokeColor(colors.HexColor('#cbd8c5'))
    canvas.line(48,38,w-48,38)
    canvas.setFillColor(MUTED)
    canvas.setFont('Body',9.5)
    canvas.drawString(48,22,'Fanze Meng | dmpoolm.github.io')
    canvas.drawRightString(w-48,22,f'{doc.page} / 2')
    canvas.restoreState()

output=ROOT/'assets'/'Fanze_Meng_Resume.pdf'
doc=SimpleDocTemplate(str(output),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=36,bottomMargin=51,title='Fanze Meng - Curriculum Vitae',author='Fanze Meng')
doc.build(story,onFirstPage=page_frame,onLaterPages=page_frame)
print(output)
