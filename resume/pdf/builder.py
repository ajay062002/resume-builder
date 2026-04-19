"""
build_resume_pdf(user) — assembles all sections and writes the PDF to disk.
Returns the file path.
"""
import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate

from .sections import (
    build_header, build_summary, build_education,
    build_skills, build_strengths, build_projects,
    build_experience, build_personal_info,
)


def _pic_path(user):
    if not user.pic:
        return None
    path = os.path.join(settings.MEDIA_ROOT, str(user.pic))
    return path if os.path.exists(path) else None


def build_resume_pdf(user):
    LM = RM = 20 * mm
    TM = BM = 15 * mm
    PAGE_W, _ = A4
    content_width = PAGE_W - LM - RM

    out_dir = os.path.join(settings.BASE_DIR, 'generated')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{user.email}.pdf')

    story = []
    story += build_header(user, content_width, _pic_path(user))
    story += build_summary(user, content_width)
    story += build_education(user, content_width)
    story += build_skills(user, content_width)
    story += build_strengths(user, content_width)
    story += build_projects(user, content_width)
    story += build_experience(user, content_width)
    story += build_personal_info(user, content_width)

    doc = SimpleDocTemplate(out_path, pagesize=A4,
                            leftMargin=LM, rightMargin=RM,
                            topMargin=TM, bottomMargin=BM)
    doc.build(story)
    return out_path
