"""Rebuild the original two-page read-aloud context partner sheet. No APIs."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'src/brainy-bucks/context-clues-practice/same-word-different-clue.pdf'
APPLE = 'https://apps.apple.com/us/app/brainy-bucks-math-reading/id6788619891'
RESOURCE = 'https://udrwu9c0tjuedqy2.github.io/hla-home/brainy-bucks/context-clues-practice/'
pdfmetrics.registerFont(TTFont('HLA', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('HLA-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
INK, PURPLE, LINE = map(HexColor, ('#282342', '#44346c', '#d7d1e4'))
BASE = ParagraphStyle('body', fontName='HLA', fontSize=11, leading=15, textColor=INK, alignment=TA_LEFT)
SMALL = ParagraphStyle('small', parent=BASE, fontSize=9, leading=13)
LARGE = ParagraphStyle('large', parent=BASE, fontSize=12, leading=17)
PAIRS = [
    ('bark', 'A dog sound', 'The outside of a tree',
     'The dog gave one loud bark when the doorbell rang.',
     'Mina rubbed the rough bark on the old tree trunk.',
     'A', 'B', 'The dog and the sound point to A.', 'The tree trunk and its rough surface point to B.'),
    ('bat', 'A flying animal', 'A piece of sports equipment',
     'Jo held the bat firmly and waited for the next pitch.',
     'At dusk, a small bat flew out of the cave.',
     'B', 'A', 'Holding it before a pitch points to B.', 'Flying out of a cave points to A.'),
    ('light', 'Not heavy', 'Something that helps us see',
     'The empty cardboard box was light enough to lift with one hand.',
     'The hallway was dark, so Ari switched on the light.',
     'A', 'B', 'Being easy to lift points to A.', 'Darkness and switching it on point to B.'),
    ('park', 'A public outdoor place', 'To leave a vehicle in a space',
     'Dad will park the car beside the shop before we walk inside.',
     'The children met at the park to use the swings.',
     'B', 'A', 'The car and where to leave it point to B.', 'Meeting outdoors by the swings points to A.'),
    ('ring', 'A sound made by a bell', 'A circular piece of jewellery',
     'The ring had a tiny blue stone and fit on one finger.',
     'The ring of the bicycle bell made us look up.',
     'B', 'A', 'The stone and finger point to B.', 'The bicycle bell and looking up point to A.'),
]

def para(c, text, x, top, width, style=BASE):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, top-h)
    return top-h

def footer(c, page):
    c.setStrokeColor(LINE); c.line(42, 45, 570, 45)
    c.setFont('HLA', 8); c.setFillColor(INK)
    c.drawString(42, 31, 'Honest Little Apps | Original web companion | No app install required')
    c.drawRightString(570, 31, f'{page} / 2')

def heading(c, eyebrow, title, subtitle):
    c.setFillColor(PURPLE); c.setFont('HLA-Bold', 9); c.drawString(42, 754, eyebrow)
    c.setFont('HLA-Bold', 25); c.drawString(42, 719, title)
    return para(c, subtitle, 42, 701, 528)

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(612, 792), pageCompression=1)
    c.setTitle('Same word, different clue - read-aloud partner sheet')
    c.setAuthor('Honest Little Apps')
    c.setSubject('Five original paired-context word meanings with a separate adult key')
    heading(c, 'BRAINY BUCKS READING COMPANION', 'Same word, different clue',
      'Partner sheet: listen, choose a meaning, then point to the clue. Grown-ups: keep the key on page 2 separate.')
    para(c, '<b>Try one pair at a time.</b> A partner may read every sentence aloud. Circle A or B for each sentence, or say the answer. Use a word, phrase or action in the sentence to explain your choice. Take a break whenever you like.', 42, 656, 528)
    c.setFillColor(HexColor('#eef6ff')); c.roundRect(42, 560, 528, 43, 6, fill=1, stroke=0)
    para(c, '<b>Example:</b> Jo gave a <b>wave</b> with her hand. Here, wave means a greeting movement. The clue is <b>with her hand</b>; it is not an ocean wave.', 52, 594, 508, SMALL)
    top = 546
    for i, (word, a, b, s1, s2, *_) in enumerate(PAIRS, 1):
        c.setStrokeColor(LINE); c.line(42, top+2, 570, top+2)
        para(c, f'<b>{i}. {word}</b> &nbsp; A: {a} &nbsp; | &nbsp; B: {b}', 42, top-6, 528, BASE)
        para(c, f'1. {s1} &nbsp; <b>A / B</b>', 54, top-29, 516, BASE)
        para(c, f'2. {s2} &nbsp; <b>A / B</b>', 54, top-51, 516, BASE)
        top -= 91
    footer(c, 1); c.showPage()
    heading(c, 'GROWN-UP KEY AND PARTNER NOTES', 'Ask for the clue',
      'The purpose is a conversation about meaning. This activity is not a reading-level test or a prediction of school results.')
    para(c, '<b>Support without rushing:</b> read the whole sentence, give time to think, and ask, "Which words helped you choose?" If an answer differs, compare the clue with both meanings. Explain an unfamiliar word first. Skip a pair if it is not useful today.', 42, 653, 528)
    top = 579
    for i, (word, a, b, s1, s2, ans1, ans2, why1, why2) in enumerate(PAIRS, 1):
        para(c, f'<b>{i}. {word} - sentence 1: {ans1}; sentence 2: {ans2}</b>', 42, top, 528, LARGE)
        para(c, f'1. {why1} &nbsp; 2. {why2}', 54, top-24, 516, BASE)
        top -= 66
    para(c, '<b>Try a transfer:</b> choose one word and say a new sentence for each meaning. The listener names the clue. An answer can be useful even when its wording differs from the key.', 42, 232, 528)
    c.setFillColor(HexColor('#f1edf7')); c.roundRect(42, 71, 528, 106, 8, fill=1, stroke=0)
    para(c, '<b>Optional next activity for grown-ups</b><br/>Honest Little Apps publishes Brainy Bucks: Math &amp; Reading. This original free companion is separate from the app. The iPhone/iPad app offers free daily quests and optional paid Plus features; check Apple for current local offers.', 54, 165, 504, SMALL)
    para(c, 'View Brainy Bucks on the App Store: <b>Apple ID 6788619891</b>', 54, 101, 504, SMALL)
    c.linkURL(APPLE, (52, 77, 560, 105), relative=0, thickness=0)
    footer(c, 2); c.save()
    print(OUT)

if __name__ == '__main__': build()
