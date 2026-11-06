"""Render the original printable and its equivalent HTML from one verified word list."""
from pathlib import Path
import html
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

base = Path(__file__).parent
output = base / "change-one-sound.pdf"
page = "https://udrwu9c0tjuedqy2.github.io/hla-home/brainy-bucks/story-order-workshop/#change-one-sound"
source = "https://ufli.education.ufl.edu/resources/teaching-resources/instructional-activities/decoding-and-encoding/"
boards = [
 ("TAP", [
  ("map", "First", "first in moon", "It shows roads."),
  ("mat", "Last", "last in hat", "It lies by a door."),
  ("sat", "First", "first in soup", "What I did on a chair yesterday."),
  ("sit", "Middle", "middle in fish", "What I can do on a chair now."),
  ("sip", "Last", "last in cup", "Take a little drink.")]),
 ("BAG", [
  ("bat", "Last", "last in hat", "It can hang upside down."),
  ("cat", "First", "first in cap", "It purrs."),
  ("cut", "Middle", "middle in sun", "What scissors do."),
  ("cup", "Last", "last in lip", "You can drink from it."),
  ("pup", "First", "first in pie", "A young dog.")])]
intro = "An adult reads each clue. The reader says the new word, then writes it in three boxes. Keep the other two sounds."
demo = "Try SUN. Change its first sound to the first sound in FAN. Blend the new word: FUN."
terms = "Families, teachers and libraries may print, photocopy or share the complete, unmodified sheet free with credit to Honest Little Apps."
for start, rows in boards:
 prev=start.lower()
 for word,pos,cue,clue in rows:
  diffs=[i for i,(a,b) in enumerate(zip(prev,word)) if a!=b]
  assert diffs==[{'First':0,'Middle':1,'Last':2}[pos]] and len(word)==len(prev)==3,(prev,word)
  prev=word

for name,f in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+f))
c=canvas.Canvas(str(output),pagesize=letter)
c.setTitle('Change one sound | Two word chains for partners')
c.setAuthor('Honest Little Apps')
ink='#172D32'; teal='#155A5C'; tint='#EEF5F2'; line='#869A97'; orange='#974829'
def txt(x,y,s,size=11,font='Sans',color=ink):
 c.setFillColor(HexColor(color)); c.setFont(font,size); c.drawString(x,y,s)
def rule(x,y,x2,color=line):c.setStrokeColor(HexColor(color));c.setLineWidth(.8);c.line(x,y,x2,y)
txt(38,752,'HONEST LITTLE APPS  /  FAMILY READING',9,'Bold',teal)
txt(38,710,'Change one sound',33,'Bold')
txt(39,687,'Two word chains for a reader and a clue giver',14,'Sans',teal)
txt(39,657,'An adult reads each clue. Say the new word, then write it in the boxes.',11)
txt(39,639,'Keep the other two sounds. Start with either word from the paper-bag play.',11)
c.setFillColor(HexColor(tint));c.roundRect(38,576,536,46,5,stroke=0,fill=1)
txt(50,603,'TRY ONE TOGETHER',8,'Bold',teal)
txt(50,586,'Say SUN. Change its first sound to the first sound in FAN. Blend it: FUN.',10,'Sans')
for i,(start,rows) in enumerate(boards):
 x=38+i*274; col=262; y=546
 txt(x,y,'Start with',11,'Sans',teal);txt(x+63,y-1,start,19,'Bold')
 rule(x,533,x+col); y=510
 for word,pos,cue,clue in rows:
  txt(x,y,pos+' sound',10,'Bold',ink)
  txt(x,y-16,'Use the '+cue+'.',9)
  txt(x,y-31,clue,9,'Sans',teal)
  for z in range(3):
   bx=x+175+z*28
   c.setStrokeColor(HexColor(teal));c.setLineWidth(.8);c.rect(bx,y-24,25,27,stroke=1,fill=0)
  rule(x,y-48,x+col); y-=64
txt(39,169,'CHECK TOGETHER',9,'Bold',orange)
txt(39,148,'TAP  →  MAP  →  MAT  →  SAT  →  SIT  →  SIP',11,'Bold')
txt(39,129,'BAG  →  BAT  →  CAT  →  CUT  →  CUP  →  PUP',11,'Bold')
txt(39,104,'If a word feels tricky, say the old word slowly, swap one sound, then blend again.',9)
rule(39,88,574)
txt(39,70,'Families, teachers and libraries may print, photocopy or share the complete, unmodified',8)
txt(39,57,'sheet free with credit to Honest Little Apps. © Honest Little Apps.',8)
txt(39,38,'Open the accessible activity and paper-bag play',9,'Bold',teal)
c.linkURL(page,(39,34,293,50),relative=0)
c.showPage();c.save()

parts=['<section class="guide" id="change-one-sound"><h2>Change one sound after the paper-bag play</h2>',
 '<p>Pick two words from the play: <strong>tap</strong> and <strong>bag</strong>. Each starts a different sound chain for a reader and a clue giver.</p>',
 '<p><a href="change-one-sound.pdf">Print the one-page word-chain board (PDF)</a></p>',
 '<details><summary>Use both word chains on screen</summary>',f'<p>{intro} {demo}</p>']
for start,rows in boards:
 parts.append(f'<h3>Start with {start.lower()}</h3><ol>')
 for _,pos,cue,clue in rows:
  parts.append(f'<li>Change the {pos.lower()} sound to the {cue}. {html.escape(clue)}</li>')
 parts.append('</ol>')
parts.extend(['<details><summary>Check the two answer chains</summary>'])
for start,rows in boards:
 parts.append('<p>'+html.escape(' → '.join([start.lower(),*[r[0] for r in rows]]))+'.</p>')
parts+=['</details><p>If a word feels tricky, say the old word slowly, swap one sound, then blend again.</p></details>',
 '<p>'+terms+'</p>',f'<p>For adults: the University of Florida Literacy Institute describes <a href="{source}">changing one sound at a time in word work</a>. The boards here are original Honest Little Apps activities.</p></section>']
(base/'section.html').write_text(''.join(parts))
