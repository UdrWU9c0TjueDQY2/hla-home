from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from pypdf import PdfReader
root=Path(__file__).parent
out=root/'emergency-kit-expiry-tracker.pdf'
c=canvas.Canvas(str(out),pagesize=(612,792));c.setTitle('Emergency Kit Expiry Tracker');c.setAuthor('Honest Little Apps')
c.setFillColor(colors.HexColor('#222222'));c.setFont('Helvetica-Bold',10);c.drawString(36,752,'FAMILY READY / PRINTABLE PLANNING SHEET')
c.setFont('Helvetica-Bold',25);c.drawString(36,713,'Emergency kit expiry tracker')
c.setFont('Helvetica',10);c.drawString(36,689,'Copy the label wording and date. Record what needs checking or replacing.')
c.drawString(36,672,'A date record is not a safety assessment. Follow the product instructions.')
c.setFont('Helvetica-Bold',10);c.drawString(36,642,'Kit / storage location:');c.line(146,639,350,639);c.drawString(375,642,'Checked on:');c.line(438,639,576,639)
xs=[36,176,296,386,576];top=615;head=32;rh=34;bottom=top-head-rh*10
c.setFillColor(colors.HexColor('#eeeeee'));c.rect(36,top-head,540,head,fill=1,stroke=0);c.setFillColor(colors.black)
c.setFont('Helvetica-Bold',9)
for x,t in zip(xs,['Item / quantity','Label wording','Date on label','Action / owner / due date']): c.drawString(x+7,top-20,t)
c.setLineWidth(.5);c.setStrokeColor(colors.HexColor('#777777'))
for x in xs:c.line(x,top,x,bottom)
c.line(36,top,576,top)
for i in range(11):y=top-head-rh*i;c.line(36,y,576,y)
c.setFont('Helvetica-Bold',10);c.drawString(36,213,'Next review:');c.line(102,210,270,210);c.drawString(300,213,'Review with:');c.line(367,210,576,210)
c.setFont('Helvetica',9)
lines=['Use the date exactly as labelled. Keep "best before", "expiry" and your own review dates distinct.',
'No date shown? Write "not shown" and check the product instructions instead of inventing one.',
'If an item or date is unclear, record a question for the manufacturer or appropriate professional.',
'Store completed sheets appropriately. You do not need to include private medical details here.']
for i,line in enumerate(lines):c.drawString(36,180-i*15,line)
c.setStrokeColor(colors.HexColor('#aaaaaa'));c.line(36,104,576,104)
c.setFont('Helvetica-Bold',9);c.drawString(36,85,'Keep the kit list with the household plan.')
c.setFont('Helvetica',8);c.drawString(36,70,'Family Ready lists a free editable kit checklist. This sheet does not scan labels or schedule reminders.')
c.drawString(36,55,'Publisher-created worksheet. Preparation only; not a complete emergency supply list.')
url='https://udrwu9c0tjuedqy2.github.io/hla-home/family-ready/kit-expiry-tracker/'
c.setFillColor(colors.HexColor('#333333'));c.drawString(36,39,url);c.linkURL(url,(36,35,576,48),relative=0)
c.showPage();c.save();r=PdfReader(out);assert len(r.pages)==1;assert 'Next review' in r.pages[0].extract_text();print(out)
