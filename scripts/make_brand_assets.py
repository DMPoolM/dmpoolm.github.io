#!/usr/bin/env python3
"""Create the original social card and multi-size favicon; optional Pillow tool."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path('/System/Library/Fonts/Supplemental')
def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)

paper, ink, green, muted = '#fafaf7', '#20352c', '#215f48', '#526458'
im = Image.new('RGB', (1200, 630), paper)
d = ImageDraw.Draw(im)
d.line((64, 42, 1136, 42), fill='#cbd8c5', width=2)
d.text((70, 78), 'RESEARCH  /  ENGINEERING  /  PERSONAL', font=font('Arial.ttf', 17), fill=green)
d.text((67, 135), 'Fanze Meng.', font=font('Georgia.ttf', 79), fill=ink)
d.text((70, 258), 'Materials, mathematics', font=font('Georgia.ttf', 39), fill=green)
d.text((70, 312), '& computing.', font=font('Georgia Italic.ttf', 39), fill=green)
d.text((70, 417), 'Institute of Science Tokyo', font=font('Arial.ttf', 23), fill=muted)
d.text((70, 451), 'A background across science and engineering.', font=font('Arial.ttf', 20), fill=muted)
nodes=[]
for z in range(3):
    for y in range(3):
        for x in range(3):
            nodes.append((x,y,z,930+(x-y)*66,282+(x+y)*29-z*75))
for x,y,z,px,py in nodes:
    for nx,ny,nz,qx,qy in nodes:
        if (nx-x,ny-y,nz-z) in [(1,0,0),(0,1,0),(0,0,1)]:
            d.line((px,py,qx,qy),fill='#9fb29f',width=2)
for x,y,z,px,py in sorted(nodes,key=lambda n:n[-1]):
    active=(x+y+z)%4==0
    r=12 if active else 8
    d.ellipse((px-r,py-r,px+r,py+r),fill=green if active else '#b2c4a5',outline=paper,width=2)
d.line((64, 549, 1136, 549), fill='#cbd8c5', width=2)
d.text((70, 575), 'dmpoolm.github.io', font=font('Arial.ttf', 21), fill=green)
im.save(ROOT/'assets'/'social-preview.png', optimize=True)

icon=Image.new('RGBA',(256,256),(0,0,0,0))
di=ImageDraw.Draw(icon)
di.rounded_rectangle((0,0,255,255),radius=51,fill=green)
di.text((38,13),'fm',font=font('Georgia Italic.ttf',153),fill=paper,stroke_width=0)
di.ellipse((208,171,223,186),fill='#d4dfc7')
icon.save(ROOT/'assets'/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64)])
print('Created social-preview.png (1200 × 630) and multi-size favicon.ico.')
