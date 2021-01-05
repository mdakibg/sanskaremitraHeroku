from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import CustomerRecord
from emitr.models import Service
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import csv

# Create your views here.
@login_required(login_url="emitr:login")
def index_view(request):
    records = CustomerRecord.objects.filter(status='Due').order_by('priority','-date')
    PaymentList = []
    for record in records:
        PaymentList.append((record.payment - record.advance))

    return render(request, 'customer/index.html', {
        'records': zip(records, PaymentList)
    })

@login_required(login_url="emitr:login")
def manage_due_view(request):
    if request.method == "POST" and "remove" in request.POST:
        CustomerRecord.objects.get(pk=request.POST["remove"]).delete()
        messages.info(request, 'Successfully Deleted Record!')
        return HttpResponseRedirect(reverse("customer:manage_due"))

    return render(request, 'customer/manage_due.html', {
        'records': CustomerRecord.objects.filter(status='Due').order_by('-date')
    })

@login_required(login_url="emitr:login")
def processing_view(request):
    records = CustomerRecord.objects.filter(status='Processing').order_by('-date')
    PaymentList = []
    for record in records:
        PaymentList.append((record.payment - record.advance))

    return render(request, 'customer/processing.html', {
        'records': zip(records, PaymentList)
    })

@login_required(login_url="emitr:login")
def manage_processing_view(request):
    if request.method == "POST" and "remove" in request.POST:
        CustomerRecord.objects.get(pk=request.POST["remove"]).delete()
        messages.info(request, 'Successfully Deleted Record!')
        return HttpResponseRedirect(reverse("customer:manage_processing"))

    return render(request, 'customer/manage_processing.html', {
        'records': CustomerRecord.objects.filter(status='Processing').order_by('-date')
    })

@login_required(login_url="emitr:login")
def completed_view(request):
    records = CustomerRecord.objects.filter(status='Done').order_by('-date')
    PaymentList = []
    for record in records:
        PaymentList.append((record.payment - record.advance))
        
    return render(request, 'customer/completed.html', {
        'records': zip(records, PaymentList)
    })

@login_required(login_url="emitr:login")
def manage_completed_view(request):
    if request.method == "POST" and "remove" in request.POST:
        CustomerRecord.objects.get(pk=request.POST["remove"]).delete()
        messages.info(request, 'Successfully Deleted Record!')
        return HttpResponseRedirect(reverse("customer:manage_completed"))

    return render(request, 'customer/manage_completed.html', {
        'records': CustomerRecord.objects.filter(status='Done').order_by('-date')
    })

@login_required(login_url="emitr:login")
def edit_view(request, request_id):
    if request.method == "POST":
        if request.POST['name'] and request.POST['mobile'] and request.POST['payment'] and request.POST['adv_payment'] and request.POST['status']:
            if int(request.POST['adv_payment']) > int(request.POST['payment']):
                messages.info(request, "Provide Valid 'Payment' Or 'Advance Payment'!")
                return HttpResponseRedirect(reverse('customer:edit', args=(request_id,)))

            record = CustomerRecord.objects.get(pk=request_id)
            record.name = request.POST["name"]
            record.mobile = request.POST["mobile"]
            record.payment = request.POST["payment"]
            record.advance = request.POST["adv_payment"]
            record.status = request.POST["status"]
            record.save()

            messages.info(request, "Updated Successfully!")
            return HttpResponseRedirect(reverse('customer:edit', args=(request_id,)))
        else:
            messages.info(request, "Please Fill All Fields!")
            return HttpResponseRedirect(reverse('customer:edit', args=(request_id,)))

    record = CustomerRecord.objects.get(pk=request_id)
    return render(request, "customer/edit.html", {
        "record" : record
    })


@login_required(login_url="emitr:login")
def create_view(request):
    if request.method == "POST":
        if request.POST['name'] and request.POST['mobile'] and request.POST['service'] and request.POST['sub_service'] and request.POST['payment'] and request.POST['adv_payment'] and request.POST['priority']:
            if int(request.POST['adv_payment']) > int(request.POST['payment']):
                messages.info(request, "Provide Valid 'Payment' Or 'Advance Payment'!")
                return HttpResponseRedirect(reverse("customer:create"))
                
            name = request.POST["name"]
            mobile = request.POST["mobile"]
            service = request.POST["service"]
            subservice = request.POST["sub_service"]
            payment = request.POST["payment"]
            advance = request.POST["adv_payment"]
            priority = request.POST["priority"]
            record = CustomerRecord(mobile=mobile, name=name, service=service, subservice=subservice, payment=payment, advance=advance, priority=priority)
            record.save()
            messages.info(request, "Successfully Created Record!")
            return HttpResponseRedirect(reverse("customer:create"))
        else:
            messages.info(request, "Please Fill All Fields!")
            return HttpResponseRedirect(reverse("customer:create"))

    services = Service.objects.all()
    all_services = list()
    for service in services:
        all_services.append({
            'name': service.title,
            'subservices': service.subservice_set.all()
        })
    return render(request, "customer/create.html", {
        'services': all_services
    })


@login_required(login_url='emitr:login')
def search_view(request):
    if request.method == "POST" and "remove" in request.POST:
        CustomerRecord.objects.get(pk=request.POST["remove"]).delete()
        messages.info(request, 'Successfully Deleted Record!')
        return HttpResponseRedirect(reverse("customer:search"))

    if request.method == "POST":
        if not request.POST["search-text"]:
            messages.info(request, 'Provide Something to Search!')
            return HttpResponseRedirect(reverse("customer:search"))

        field = request.POST['search-field']
        search_text = request.POST['search-text']
        
        if field == 'mobile':
            results = CustomerRecord.objects.filter(mobile__contains=search_text)
        else:
            results = CustomerRecord.objects.filter(name__icontains=search_text)

        if not results:
            messages.info(request, 'No Result(s) Found!')
            return HttpResponseRedirect(reverse("customer:search"))

        return render(request, 'customer/search.html', {
            'results': results
        })

    return render(request, "customer/search.html")

@login_required(login_url='emitr:login')
def csv_view(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Name', 'Mobile', 'Service', 'Sub-Service', 'Payment', 'Advance', 'Priority', 'Status', 'Date'])

    for record in CustomerRecord.objects.all().values_list('name', 'mobile', 'service', 'subservice', 'payment', 'advance', 'priority', 'status', 'date'):
        writer.writerow(record)

    response['Content-Disposition'] = 'attachment; filename="CusomterRecord.csv"'

    return response