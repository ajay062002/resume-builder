from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle

BLACK  = HexColor('#000000')
DARK   = HexColor('#1a1a1a')
GREY   = HexColor('#444444')

def make_style(name, **kw):
    kw.setdefault('fontName', 'Helvetica')
    kw.setdefault('textColor', DARK)
    kw.setdefault('fontSize', 10)
    kw.setdefault('leading', 14)
    return ParagraphStyle(name, **kw)

name_style    = make_style('nm', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=BLACK)
contact_style = make_style('ct', fontSize=9, textColor=GREY, leading=13, spaceAfter=4)
section_style = make_style('sh', fontName='Helvetica-Bold', fontSize=11, textColor=BLACK,
                            leading=14, spaceBefore=10, spaceAfter=2)
body_style    = make_style('bd', fontSize=9.5, textColor=DARK, leading=14)
bullet_style  = make_style('bl', fontSize=9.5, textColor=DARK, leading=14,
                            leftIndent=12, firstLineIndent=-12, spaceAfter=2)
label_style   = make_style('lb', fontName='Helvetica-Bold', fontSize=9.5, textColor=DARK, leading=14)
skill_style   = make_style('sk', fontSize=9.5, textColor=DARK, leading=14)
