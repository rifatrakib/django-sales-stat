from django.shortcuts import render
from django.http import JsonResponse

from .models import Report
from .forms import ReportForm
from .utils import get_report_image

from profiles.models import Profile


def create_report_view(request):
    form = ReportForm(request.POST or None)
    if request.is_ajax():
        # name = request.POST.get('name')
        # remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.image = img
            form_instance.author = author
            form_instance.save()
        # Report.objects.create(
            # name=name, remarks=remarks, image=img, author=author,)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({'error': 'something went wrong'})
