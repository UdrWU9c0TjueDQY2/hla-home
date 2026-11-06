"""Build the original two-page family communication tabletop (no personal data)."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'src/family-ready/7-day-family-emergency-plan-challenge/contact-ladder-tabletop.pdf'
APP='https://apps.apple.com/us/app/family-ready-emergency-plan/id6792019825'
GUIDE='https://udrwu9c0tjuedqy2.github.io/hla-home/family-ready/7-day-family-emergency-plan-challenge/#tabletop'
SOURCE='https://www.canada.ca/en/services/policing/emergencies/preparedness/get-prepared/make-plan/emergency-plan-form.html'
FONTDIR=Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('Body',str(FONTDIR/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('Bold',str(FONTDIR/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Serif',str(FONTDIR/'DejaVuSerif.ttf')))
W,H=595.276,841.89
INK=HexColor('#182f3b');TEAL=HexColor('#155d66');PALE=HexColor('#eaf2ef');LINE=HexColor('#b4c6c7')
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('Who gets the message? A family communication tabletop')
c.setAuthor('Honest Little Apps');c.setSubject('Original fictional communication practice and contact ladder; not an emergency-response service')
def text(x,y,value,font='Body',size=10.2,color=INK):
 c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,value)
def para(x,y,value,width=499,size=10.2,leading=15,font='Body'):
 for line in simpleSplit(value,font,size,width):text(x,y,line,font,size);y-=leading
 return y
def header(num,kicker,title):
 c.setFillColor(TEAL);c.rect(0,H-13,W,13,fill=1,stroke=0)
 text(48,H-44,'HONEST LITTLE APPS / FAMILY READY','Bold',9,TEAL)
 text(W-98,H-44,f'{num} / 2','Bold',9,TEAL)
 text(48,H-78,kicker,'Bold',10)
 text(48,H-112,title,'Serif',25)
def footer(num):
 c.setStrokeColor(LINE);c.line(48,54,W-48,54)
 text(48,38,'Original exercise by Honest Little Apps. Free to print and share intact with credit.','Body',7.4)
 text(W-71,38,str(num),'Bold',8)
header(1,'FICTIONAL TABLETOP / OPTIONAL 10-MINUTE PRACTICE','Who gets the message?')
y=para(48,H-139,'Alex and Sam are safely in different places. Robin is their agreed out-of-town contact. No one is in danger. Work out how a short check-in reaches everyone when one part of the plan is unavailable.')
y=para(48,y-4,'Discuss only. Do not call emergency services, send test alerts or share real contact details. Anyone can pass. An adult facilitates household practice; use local official instructions in a real emergency.',size=9.2,leading=13)
text(48,y-19,'PLAY IN THREE STEPS','Bold',10,TEAL)
y=para(48,y-38,'1. Choose who reads Alex, Sam and Robin. One person can cover more than one role.')
y=para(48,y-2,'2. Read one card. Say the next contact attempt, what the message needs, and how you will know it arrived.')
y=para(48,y-2,'3. Turn over one more card. Change the plan if needed. Finish with one update on page 2.')
cards=[
 ('A / CALLS DO NOT CONNECT','Alex can send a text, but voice calls do not connect. What brief check-in could Alex send to the agreed contact? What would count as a reply?'),
 ('B / ONE PHONE IS FLAT','Sam cannot use a phone. Which paper copy or agreed helper could Sam use? Where would Sam find the information without relying on that phone?'),
 ('C / THE USUAL CONTACT IS UNAVAILABLE','Robin does not answer. What backup contact or next step was agreed beforehand? How would Alex and Sam learn the same update?'),
 ('D / TWO COPIES DISAGREE','A printed contact card is older than the household plan. Who checks the details, dates the revision and replaces the copies that need updating?')]
y-=10
for title,body in cards:
 c.setFillColor(PALE);c.roundRect(48,y-86,W-96,86,7,fill=1,stroke=0)
 text(61,y-18,title,'Bold',9.4,TEAL)
 para(61,y-36,body,width=W-122,size=9.3,leading=13)
 y-=96
footer(1);c.showPage()
header(2,'KEEP THE DECISIONS / REVIEW TOGETHER','Make one useful change')
y=para(48,H-139,'There is no winning score and no guaranteed delivery method. The useful result is a shared next step, a way to confirm a message arrived, and a current copy people can find.')
text(48,y-20,'THE CONTACT LADDER','Bold',10,TEAL)
rows=[('1  FIRST ATTEMPT','Agreed contact role and preferred channel:'),('2  IF UNAVAILABLE','Backup contact or next agreed step:'),('3  PAPER / OFFLINE COPY','Where a current copy can be found without this phone:'),('4  CLOSE THE LOOP','What reply confirms receipt, and who passes on the update:')]
y-=37
for label,prompt in rows:
 text(48,y,label,'Bold',9.3,TEAL);text(48,y-18,prompt,'Body',9.3)
 c.setStrokeColor(LINE);c.line(48,y-40,W-48,y-40);y-=66
text(48,y-8,'ONE UPDATE BEFORE YOU FINISH','Bold',10,TEAL)
y=para(48,y-28,'Our next change: ______________________________________________________\nPerson who will check it: __________________  Review date: ______________',size=9.5,leading=19)
text(48,y-18,'FACILITATOR NOTES','Bold',10,TEAL)
y=para(48,y-36,'A: Keep the message brief; a sent message is not a confirmed reply. B: Find a usable paper copy or agreed support person. C: Agree the backup in advance rather than assuming everyone knows it. D: Check details with the people concerned and date replacement copies. These are discussion prompts, not emergency procedures.',size=8.7,leading=12)
y=para(48,y-4,'Planning basis: Public Safety Canada, Make an emergency plan, steps 2 and 7: meeting places, household contacts and an out-of-town contact. Guidance checked November 5, 2026. This independent exercise is not a government publication.',size=8,leading=11)
c.linkURL(SOURCE,(48,y, W-48,y+40),relative=0,thickness=0)
text(48,y-16,'Read the official planning form','Bold',8,TEAL);c.linkURL(SOURCE,(48,y-19,230,y-6),relative=0,thickness=0)
y-=40
icon=ROOT/'src/assets/family-ready/icon-128.webp'
c.drawImage(ImageReader(str(icon)),48,y-36,36,36,mask='auto')
text(95,y-3,'Optional continuation: Family Ready on iPhone','Bold',9,TEAL)
para(95,y-19,'Free Emergency Card, household plan and Snapshot PDF. Optional Plus adds sharing and extra packs. This paper exercise does not sync to the app.',width=W-145,size=8.2,leading=11)
c.linkURL(APP,(48,y-42,W-48,y+8),relative=0,thickness=0)
text(48,y-58,APP,'Body',7.4,TEAL);c.linkURL(APP,(48,y-61,W-48,y-48),relative=0,thickness=0)
text(48,y-74,'Free guide and text alternative: open the original challenge page, section "Tabletop".','Body',7.4,TEAL)
c.linkURL(GUIDE,(48,y-78,W-48,y-63),relative=0,thickness=0)
footer(2);c.save()
print(OUT)
