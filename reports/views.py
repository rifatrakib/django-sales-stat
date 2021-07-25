from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.dateparse import parse_date

from .models import Report
from .forms import ReportForm
from .utils import get_report_image

from profiles.models import Profile
from customers.models import Customer
from products.models import Product
from sales.models import Sale, Position, CSV

from xhtml2pdf import pisa

import csv


class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'


def csv_upload_view(request):
    print('file is being sent')
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(
                            name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(
                            product=product_obj, quantity=quantity, created=date)
                        sales_obj, _ = Sale.objects.get_or_create(
                            transaction_id=transaction_id, customer=customer_obj,
                            salesman=salesman_obj, created=date)
                        sales_obj.positions.add(position_obj)
                        sales_obj.save()
                return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex': True})
    return HttpResponse('Hello')


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


def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    # obj = Report.objects.get(pk=pk)
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # use this option for direct download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # use this option for viewing as pdf
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
