from django.http import FileResponse
from resume.models import UserModel
from resume.pdf import build_resume_pdf


def download(request):
    user = UserModel.objects.filter(email=request.GET.get('email')).first()
    if not user:
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound('User not found')

    pdf_path = build_resume_pdf(user)
    filename = f'{user.name or user.email}_resume.pdf'
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
