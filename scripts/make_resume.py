#!/usr/bin/env python3
"""Regenerate the website's public resume. Requires reportlab (optional for site builds)."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content.json').read_text())
INK=colors.HexColor('#20352c')
GREEN=colors.HexColor('#215f48')
MUTED=colors.HexColor('#58665d')
styles={
 'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=INK,spaceAfter=6),
 'contact':ParagraphStyle('contact',fontName='Helvetica',fontSize=8.5,leading=13,textColor=MUTED),
 'intro':ParagraphStyle('intro',fontName='Helvetica',fontSize=9.2,leading=13.2,textColor=INK,spaceAfter=11),
 'section':ParagraphStyle('section',fontName='Helvetica-Bold',fontSize=9,leading=13,textColor=GREEN,spaceBefore=11,spaceAfter=6),
 'heading':ParagraphStyle('heading',fontName='Helvetica-Bold',fontSize=9.3,leading=12.8,textColor=INK),
 'date':ParagraphStyle('date',fontName='Helvetica',fontSize=8.2,leading=12.8,textColor=MUTED,alignment=2),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=8.8,leading=12.5,textColor=INK,spaceAfter=5),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=8.8,leading=12.5,textColor=INK,leftIndent=9,firstLineIndent=-9,spaceAfter=4),
}
story=[]
def p(text,style='body'):
 return Paragraph(text,styles[style])
def section(name): story.append(p(name.upper(),'section'))
def row(label,date):
 t=Table([[p(label,'heading'),p(date,'date')]],colWidths=[368,143])
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
 story.append(t)
def bullet(text): story.append(p('• '+text,'bullet'))

story.append(p('Fanze Meng','name'))
story.append(p('Japan | <link href="mailto:'+data['email']+'">'+data['email']+'</link>','contact'))
story.append(p('<link href="'+data['github']+'">github.com/DMPoolM</link> | <link href="'+data['linkedin']+'">LinkedIn</link>','contact'))
story.append(Spacer(1,12))
story.append(p('Computational materials MSc student with training in materials science and engineering mathematics. Experience in materials property prediction, uncertainty estimation, research software, and generative AI for industrial engineering.','intro'))

section('Education')
for e in data['education']:
 row(e['school'],e['date'].replace('–','-'))
 story.append(p(e['degree'].replace('·','|').replace('–','-'),'body'))

section('Selected research and engineering experience')
row('Volvo Cars | Materials &amp; AI internship','Feb 2025 - Jan 2026')
bullet('Built CNN-Transformer models to predict stress-strain curves from microstructure images of 90 representative volume elements, reaching validation R<super>2</super> = 0.89; estimated uncertainty with Monte Carlo dropout.')
bullet('Developed Material Centre, a Streamlit and Plotly application for materials similarity search using PCA and distance metrics; containerised with Docker and deployed for internal user testing.')
bullet('Developed a physics-informed model variant with elastic-modulus, smoothness, and boundary-condition losses.')
story.append(Spacer(1,5))
row('Tohoku University | COLABS research exchange','Sep 2024 - Feb 2025')
bullet('Built a graph-similarity clustering pipeline for 3D electron diffraction structure candidates, reducing the number requiring manual verification by 97.2% on average across 7 datasets (2,127 structures).')
bullet('Replicated a catalyst-screening study using pretrained FAIR-Chem GNN models; generated adsorbate-slab configurations, ran ML relaxations, and compared adsorption energies with literature values.')
story.append(Spacer(1,5))
row('Institute of Science Tokyo | MSc research','Oct 2026 - present')
bullet('Developing physics-aware generative models to reconstruct 3D atomic structures from pair distribution functions, targeting solid electrolytes for batteries.')
story.append(Spacer(1,5))
row('Chalmers × Volvo Cars | MSc thesis','Oct 2025 - Jun 2026')
bullet('Co-developed an LLM agent with retrieval over ABB manuals to generate RAPID robot code; implemented an HPC-based validation framework and benchmarked on approximately 50 manufacturing tasks.')

section('Technical skills and languages')
story.append(p('<b>ML and software:</b> Python, PyTorch, TensorFlow, scikit-learn, XGBoost; CNNs, GNNs, PINNs; uncertainty estimation, LLM agents, RAG; Git, Docker, Azure, Streamlit, Plotly.'))
story.append(p('<b>Materials:</b> FAIR-Chem, ASE, RDKit; XRD, IR spectroscopy, SEM, electrochemical testing.'))
story.append(p('<b>Languages:</b> Chinese (native); English (fluent, IELTS 7.5); Japanese (actively studying).'))

section('Selected publications')
story.append(p('Second author: <i>Nano Today</i> (2023), doi: <link href="https://doi.org/10.1016/j.nantod.2023.101766">10.1016/j.nantod.2023.101766</link>.'))
story.append(p('Second author: <i>Journal of Physics: Conference Series</i> (2021), doi: <link href="https://doi.org/10.1088/1742-6596/2021/1/012021">10.1088/1742-6596/2021/1/012021</link>.'))

output=ROOT/'assets'/'Fanze_Meng_Resume.pdf'
doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=33,bottomMargin=31,title='Fanze Meng - Resume',author='Fanze Meng')
doc.build(story)
print(output)
