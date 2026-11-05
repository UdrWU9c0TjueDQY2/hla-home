from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'src/family-ready/offline-card-access-check'
OUT = PAGE / 'household-meeting-point-wallet-cards.pdf'
WEB = 'https://udrwu9c0tjuedqy2.github.io/hla-home/family-ready/offline-card-access-check/#meeting-point-cards'
APPLE = 'https://apps.apple.com/us/app/family-ready-emergency-plan/id6792019825'
INK = HexColor('#222e35')
ACCENT = HexColor('#263e46')
LIGHT = HexColor('#e0e6df')
RULE = HexColor('#75818a')
pdfmetrics.registerFont(TTFont('CardSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('CardSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

c = canvas.Canvas(str(OUT), pagesize=(612, 792), invariant=1, pageCompression=1)
c.setTitle('Household Meeting-Point Wallet Cards | Honest Little Apps')
c.setAuthor('Honest Little Apps')
c.setSubject('Original blank household planning cards with two meeting places, a chosen contact and a review date.')

def text(x, y, body, size=10, font='Helvetica', width=522, leading=None, color=INK):
    font = 'CardSans-Bold' if font.endswith('Bold') else 'CardSans'
    c.setFillColor(color)
    c.setFont(font, size)
    lines = simpleSplit(body, font, size, width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading or size * 1.4
    return y

def line(x1, y, x2):
    c.setStrokeColor(RULE)
    c.setLineWidth(.45)
    c.line(x1, y, x2, y)

c.setFillColor(ACCENT)
c.rect(0, 756, 612, 36, fill=1, stroke=0)
text(45, 768, 'HONEST LITTLE APPS  /  FAMILY PLANNING', 10, 'Helvetica-Bold', color=white)
text(45, 719, 'A meeting plan that fits in a wallet.', 23, 'Helvetica-Bold')
text(45, 690, 'Two blank copies. One agreed plan. No app or sign-up needed.', 11)
text(45, 662, 'Agree on appropriate meeting places and a contact with your household. Check access needs and local instructions. Fill in these cards privately, then give each copy to its intended person.', 10.5, width=522)
text(45, 612, 'Print at 100% / Actual size. Each cut card is 3.5 x 2.25 in (89 x 57 mm).', 9.5, 'Helvetica-Bold')
text(45, 596, 'Cut on the outside dotted line. Do not enter door codes, passwords or identity numbers.', 9.5)

def card(x, y, number):
    w, h = 252, 162
    c.setDash(2, 2)
    c.setLineWidth(.7)
    c.setStrokeColor(INK)
    c.roundRect(x, y, w, h, 5, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(LIGHT)
    c.rect(x+1, y+h-27, w-2, 26, fill=1, stroke=0)
    text(x+10, y+h-17, 'HOUSEHOLD MEETING PLAN', 10, 'Helvetica-Bold', width=w-20)
    # Space for handwriting is deliberately larger than the label text.
    for label, dy in [('NEARBY MEETING PLACE', 43), ('OUTSIDE-AREA / ALTERNATE PLACE', 72), ('CHOSEN CONTACT (AGREED IN ADVANCE)', 101)]:
        text(x+10, y+h-dy, label, 7.5, 'Helvetica-Bold', width=w-20)
        line(x+10, y+h-dy-14, x+w-10)
    text(x+10, y+32, 'PHONE', 7.5, 'Helvetica-Bold')
    line(x+45, y+29, x+w-10)
    text(x+10, y+15, 'CHECKED', 7.2, 'Helvetica-Bold')
    line(x+57, y+12, x+119)
    text(x+129, y+15, 'REVIEW', 7.2, 'Helvetica-Bold')
    line(x+171, y+12, x+w-10)
    text(x, y-17, f'Copy {number}: keep where its intended person can find it.', 8.5, width=w)

card(45, 412, 1)
card(315, 412, 2)

text(45, 369, 'Before you carry the cards', 15, 'Helvetica-Bold')
items = [
    ('1  Agree', 'Choose places you can identify clearly. Consider a nearby location and one outside your immediate area. Agree who will receive and relay household updates; an out-of-town contact may help.'),
    ('2  Check', 'Confirm the contact details with the person concerned. Check school, workplace and local emergency instructions. This card does not authorize a child pickup or override an evacuation direction.'),
    ('3  Practice', 'At a calm time, find the card and point to both places on a map. Explain what you would do if a place were inaccessible. Do not make emergency calls or travel into danger for a practice.'),
]
y = 343
for title, body in items:
    text(45, y, title, 10.5, 'Helvetica-Bold', width=62)
    y = text(117, y, body, 9.7, width=450, leading=13) - 14

y = min(y-3, 182)
text(45, y, 'What needs changing after your practice?', 10, 'Helvetica-Bold')
line(45, y-20, 567)
line(45, y-40, 567)
text(45, y-62, 'A practical planning aid, not a complete emergency plan or a guarantee of access or safety. Follow local authorities. Move to a meeting place only when it is safe to do so.', 9.3, width=522)

text(45, 78, 'Sources: Public Safety Canada, Make an Emergency Plan; ISED Canada,', 8.5)
text(45, 66, 'Create an emergency telecommunications plan. Links and full HTML equivalent:', 8.5)
text(45, 54, 'hla-home/family-ready/offline-card-access-check/#meeting-point-cards', 8.5, color=ACCENT)
c.linkURL(WEB, (45, 49, 567, 63), relative=0)
text(45, 31, 'Honest Little Apps publishes Family Ready. Optional iPhone app: free core, paid Plus.', 8.5)
c.linkURL(APPLE, (45, 26, 567, 42), relative=0)
c.save()

page = PAGE / 'index.html'
html = page.read_text()
if 'id="meeting-point-cards"' in html:
    print(OUT)
    raise SystemExit(0)
style = '''
.meeting-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;margin:25px 0}.meeting-card{min-width:0;padding:22px;border:2px dashed #75818a;background:#fffdf5;border-radius:8px}.meeting-card h3{font-size:20px}.meeting-card dl{margin:0}.meeting-card dt{font-weight:bold;font-size:16px;margin-top:17px}.meeting-card dd{margin:4px 0 0;padding:5px 0 10px;border-bottom:1px solid #75818a;font-size:16px;color:#58636a;overflow-wrap:anywhere}.meeting-guide li{margin-bottom:13px}.pdf-link{display:inline-block;padding:14px 18px;border:2px solid #263e46;border-radius:5px;font-weight:bold;line-height:1.35}.meeting-source{font-size:15px}.meeting-source a{overflow-wrap:anywhere}@media(max-width:730px){.meeting-cards{grid-template-columns:1fr}.meeting-card{padding:18px}}@media print{.meeting-cards{display:block}.meeting-card{break-inside:avoid;margin:12px 0}.pdf-link{display:none}}
'''
html = html.replace('</style>', style + '</style>', 1)
card_html = '''<article class="meeting-card" aria-label="Blank meeting plan card {n}"><h3>Copy {n}: household meeting plan</h3><dl><dt>Nearby meeting place</dt><dd>Write an agreed, clearly identifiable place.</dd><dt>Outside-area or alternate place</dt><dd>Write an agreed alternative and how to identify it.</dd><dt>Chosen contact</dt><dd>Write the name of someone who agreed to receive updates.</dd><dt>Phone</dt><dd>Write the number you checked with that person.</dd><dt>Last checked</dt><dd>Write the date you confirmed this information.</dd><dt>Next review</dt><dd>Write a review date agreed by your household.</dd></dl></article>'''
section = '''<section class="section" id="meeting-point-cards" aria-labelledby="meeting-point-title"><div class="eyebrow">Free printable / two wallet-size copies</div><h2 id="meeting-point-title">Carry the same meeting plan.</h2><p class="intro">A charged phone is one way to keep a plan handy. These original blank cards give two household members a paper copy of the meeting places and contact they have agreed on. They are a practical planning aid, separate from Family Ready's app and its Emergency Snapshot PDF.</p><p><a class="pdf-link" href="household-meeting-point-wallet-cards.pdf" type="application/pdf">Download the two-card sheet (PDF, one page)</a></p><p class="small">US Letter. Print at 100% or Actual size, then cut on the dotted lines. Each card is 3.5 x 2.25 inches (89 x 57 mm). No signup or app is needed. Fill in the paper privately; this page has no fields for your contacts or locations.</p><div class="meeting-cards">''' + card_html.format(n=1) + card_html.format(n=2) + '''</div><h3>A calm review, before the cards are needed</h3><ol class="meeting-guide"><li><strong>Agree on the places and contact.</strong> Consider a nearby meeting place and one outside your immediate area. Check that the locations fit your household's access needs. An out-of-town contact can help relay updates if local communications are disrupted.</li><li><strong>Check the details together.</strong> Confirm the contact number with the person concerned. Keep school and workplace emergency procedures in mind. This card does not authorize a child pickup or override evacuation instructions.</li><li><strong>Practice finding the plan.</strong> At a convenient time, find the card and point to both places on a map. Explain what you would do if a place were inaccessible. Do not call an emergency number or travel into danger as a test.</li><li><strong>Write a review date.</strong> Note anything that needs changing after the discussion. Recheck the cards when a location, phone number or household need changes. Give updated copies only to the appropriate people.</li></ol><p class="rule">Follow instructions from local authorities. Move to a meeting place only when it is safe. A card cannot guarantee that a place, route, contact or communications network will be available. Keep door codes, passwords and identity numbers off a card that could be seen by others.</p><p class="meeting-source">The card layout and review exercise are original work from Honest Little Apps. Planning concepts come from <a href="https://www.canada.ca/en/services/policing/emergencies/preparedness/get-prepared/make-plan.html">Public Safety Canada: Make an Emergency Plan</a> and <a href="https://ised-isde.canada.ca/site/emergency-communications/en/create-emergency-telecommunications-plan">ISED Canada: Create an emergency telecommunications plan</a>, read 5 November 2026. They recommend agreed meeting places, an out-of-town contact, paper copies and practice. This printable is not an official government template and has no government endorsement. The full fields, instructions and limitations are available above as HTML.</p></section>
'''
anchor = '<section class="section"><h2>Free card. Optional sharing features.</h2>'
assert html.count(anchor) == 1
html = html.replace(anchor, section+anchor, 1)
html = html.replace('Publisher-created guide · Updated 4 November 2026', 'Publisher-created guide · Updated 5 November 2026')
page.write_text(html)
print(OUT)
