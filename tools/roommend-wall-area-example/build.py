from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

out = Path(sys.argv[1])
im = Image.new("RGB", (1000,1500), "#fcf5e9")
d = ImageDraw.Draw(im)
dark, green, terra, pale = "#193633", "#22594e", "#984526", "#e6eee7"
regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def label(x,y,t,size=32,colour=dark,face=regular):
    font = ImageFont.truetype(face,size)
    assert x + font.getlength(t) <= 968, t
    d.text((x,y),t,font=font,fill=colour,anchor="lt")

d.rectangle((0,0,999,254),fill=dark)
label(60,32,"ROOMMEND  /  PROJECT NOTES",25,"#bad9c8",bold)
label(56,87,"How much wall",63,"#fff5db",serif)
label(56,162,"will you paint?",63,"#fff5db",serif)
label(60,300,"Unfold all four walls",43,face=bold)
label(60,359,"A 4 m × 3 m room with 2.4 m walls",34)
x,y,scale=72,469,61
for i,m in enumerate([4,3,4,3]):
    w=m*scale
    d.rectangle((x,y,x+w,y+146),fill=["#b6d1bd","#95bca6"][i%2],outline=dark,width=3)
    label(x+(w-60)//2,426,f"{m} m",28)
    if i==0: # 0.9 m wide and 2 m tall, aligned with floor
        d.rectangle((x+78,y+146-122,x+78+55,y+146),fill="#fcf5e9",outline=terra,width=4)
    if i==1: # 2 m wide by 1.1 m tall
        d.rectangle((x+30,y+41,x+152,y+108),fill="#fcf5e9",outline=terra,width=4)
    x+=w
label(72,642,"14 m around × 2.4 m high = 33.6 m²",34,green,bold)
d.line((60,710,940,710),fill="#b6b9a9",width=2)
label(60,751,"Subtract the openings once",41,face=bold)
label(60,833,"Door",30,terra,bold)
label(284,833,"0.9 × 2 m",33)
label(661,833,"1.8 m²",33,face=bold)
label(60,911,"Window",30,terra,bold)
label(284,911,"2 × 1.1 m",33)
label(661,911,"2.2 m²",33,face=bold)
d.rectangle((60,993,940,1077),fill=pale)
label(85,1015,"33.6 − 1.8 − 2.2 = 29.6 m² per coat",34,green,bold)
label(60,1123,"Apply the label coverage",40,face=bold)
label(60,1197,"29.6 m² × 2 coats ÷ 10 m²/L",38)
label(60,1262,"= 5.92 litres",60,terra,serif)
label(60,1371,"Example only. Use your paint’s per-coat coverage.",29)
label(60,1420,"Walls only. Excludes primer, trim and waste.",28)
im.save(out, optimize=True)
