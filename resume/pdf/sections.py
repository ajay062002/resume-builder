"""
Each function builds one resume section and returns a list of ReportLab flowables.
"""
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage
from reportlab.lib.styles import ParagraphStyle

from .styles import (
    BLACK, DARK,
    name_style, contact_style, section_style,
    body_style, bullet_style, label_style, skill_style,
)


def val_ok(v):
    return v and str(v).strip() not in ('', 'None', 'none')


def section_header(title, page_width):
    return [
        Paragraph(f'<u><b>{title}</b></u>', section_style),
        HRFlowable(width=page_width, thickness=0.6, color=BLACK, spaceAfter=5),
    ]


def two_col_row(left, right, page_width):
    label_w = 48 * mm
    return Table(
        [[Paragraph(f'<b>{left}</b>', label_style), Paragraph(str(right), body_style)]],
        colWidths=[label_w, page_width - label_w],
        style=TableStyle([
            ('VALIGN',         (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING',     (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING',  (0, 0), (-1, -1), 2),
            ('LEFTPADDING',    (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',   (0, 0), (-1, -1), 0),
        ])
    )


def bullet_para(text):
    return Paragraph(f'• &nbsp;{text}', bullet_style)


def build_header(user, page_width, pic_path=None):
    name_block = [Paragraph(str(user.name or ''), name_style)]

    contacts = [c for c in [
        str(user.email) if val_ok(user.email) else None,
        str(user.mobile) if val_ok(user.mobile) else None,
        str(user.address) if val_ok(user.address) else None,
    ] if c]
    if contacts:
        name_block.append(Paragraph('   |   '.join(contacts), contact_style))

    if pic_path:
        img = RLImage(pic_path, width=28 * mm, height=28 * mm)
        hdr = Table(
            [[name_block, img]],
            colWidths=[page_width - 32 * mm, 32 * mm],
            style=TableStyle([
                ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN',         (1, 0), (1, 0),   'RIGHT'),
                ('LEFTPADDING',   (0, 0), (-1, -1), 0),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
                ('TOPPADDING',    (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])
        )
        return [hdr, HRFlowable(width=page_width, thickness=1.2, color=BLACK, spaceAfter=6)]
    else:
        return name_block + [HRFlowable(width=page_width, thickness=1.2, color=BLACK, spaceAfter=6)]


def build_summary(user, page_width):
    if not val_ok(user.careerobjective):
        return []
    flowables = section_header('Professional Summary', page_width)
    for line in str(user.careerobjective).split('\n'):
        if line.strip():
            flowables.append(bullet_para(line.strip()))
    flowables.append(Spacer(1, 4))
    return flowables


def build_education(user, page_width):
    rows = []
    if val_ok(user.degreebranch) or val_ok(user.degreepercentage):
        label = str(user.degreebranch or '')
        pct   = (' — ' + str(user.degreepercentage) + '%') if val_ok(user.degreepercentage) else ''
        rows.append(('Degree', label + pct))
    if val_ok(user.intermediatebranch) or val_ok(user.intermediatepercentage):
        label = str(user.intermediatebranch or '')
        pct   = (' — ' + str(user.intermediatepercentage) + '%') if val_ok(user.intermediatepercentage) else ''
        rows.append(('Intermediate (12th)', label + pct))
    if val_ok(user.sscpercentage):
        rows.append(('SSC (10th)', str(user.sscpercentage) + '%'))
    if not rows:
        return []
    flowables = section_header('Education', page_width)
    for lbl, val in rows:
        flowables.append(two_col_row(lbl, val, page_width))
    flowables.append(Spacer(1, 4))
    return flowables


def build_skills(user, page_width):
    if not val_ok(user.skills):
        return []
    skills_list = [s.strip() for s in str(user.skills).replace('\n', ',').split(',') if s.strip()]
    if not skills_list:
        return []

    cols = 3
    col_w = page_width / cols
    rows_data, row = [], []
    for sk in skills_list:
        row.append(Paragraph(f'• {sk}', skill_style))
        if len(row) == cols:
            rows_data.append(row)
            row = []
    if row:
        while len(row) < cols:
            row.append(Paragraph('', skill_style))
        rows_data.append(row)

    table = Table(rows_data, colWidths=[col_w] * cols,
        style=TableStyle([
            ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING',    (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING',   (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
        ]))

    flowables = section_header('Technical Skills', page_width)
    flowables += [table, Spacer(1, 4)]
    return flowables


def build_strengths(user, page_width):
    if not (val_ok(user.personalstrengths) or val_ok(user.professionalstrengths)):
        return []
    flowables = section_header('Key Strengths', page_width)
    if val_ok(user.personalstrengths):
        flowables.append(two_col_row('Personal', str(user.personalstrengths), page_width))
    if val_ok(user.professionalstrengths):
        flowables.append(two_col_row('Professional', str(user.professionalstrengths), page_width))
    flowables.append(Spacer(1, 4))
    return flowables


def build_projects(user, page_width):
    if not (val_ok(user.projecttitle) or val_ok(user.projectdescription)):
        return []
    flowables = section_header('Projects', page_width)
    if val_ok(user.projecttitle):
        flowables.append(Paragraph(f'<b>{user.projecttitle}</b>', body_style))
    if val_ok(user.projectdescription):
        for line in str(user.projectdescription).split('\n'):
            if line.strip():
                flowables.append(bullet_para(line.strip()))
    flowables.append(Spacer(1, 4))
    return flowables


def build_experience(user, page_width):
    if not (val_ok(user.currentworkingcompany) or val_ok(user.yearofExperience)):
        return []
    flowables = section_header('Professional Experience', page_width)
    if val_ok(user.currentworkingcompany):
        flowables.append(Paragraph(f'<b>Current Company:</b> {user.currentworkingcompany}', body_style))
    if val_ok(user.yearofExperience):
        flowables.append(Paragraph(f'<b>Years of Experience:</b> {user.yearofExperience}', body_style))
    flowables.append(Spacer(1, 4))
    return flowables


def build_personal_info(user, page_width):
    fields = [
        ('Date of Birth', user.dob),
        ('Gender',        user.gender),
        ('Nationality',   user.nationality),
        ('Languages',     user.languages),
    ]
    rows = [(lbl, val) for lbl, val in fields if val_ok(val)]
    if not rows:
        return []
    flowables = section_header('Personal Information', page_width)
    for lbl, val in rows:
        flowables.append(two_col_row(lbl, str(val), page_width))
    return flowables
