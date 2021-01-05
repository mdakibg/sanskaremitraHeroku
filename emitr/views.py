from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Service, SubService
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Create your views here.

def index(request):
    if request.method == "POST":
        if not request.POST['search-term']:
            messages.info(request, 'Provide search term!')
            return render(request, 'emitr/search_results.html')

        search_term = request.POST['search-term']
        subservices = SubService.objects.filter(name__icontains=search_term)
        services = Service.objects.filter(title__icontains=search_term)

        if services and not subservices:
            ServiceResults = list()
            for service in services:
                for subservice in service.subservice_set.all():
                    ServiceResults.append({
                        'name': service.title,
                        'subservice': subservice.name,
                        'fee': subservice.fee
                    })
            return render(request, 'emitr/search_results.html', {
                'ServiceResults': ServiceResults,
                "search_term": search_term
            })
        elif subservices and not services:
            return render(request, 'emitr/search_results.html', {
                'SubServiceResults': subservices,
                "search_term": search_term
            })
        elif services and subservices:
            ServiceResults = list()
            for service, subservice in zip(services, subservices):
                if not service.subservice_set.filter(name=subservice.name):
                    for subservice in service.subservice_set.all(): 
                        ServiceResults.append({
                            'name': service.title,
                            'subservice': subservice.name,
                            'fee': subservice.fee
                        })
            return render(request, 'emitr/search_results.html', {
                'SubServiceResults': subservices,
                'ServiceResults': ServiceResults,
                "search_term": search_term
            })
        else:
          messages.info(request, 'No Results Found!')
          return render(request, 'emitr/search_results.html', {
              'search_term': search_term
          })


    services = list()
    for service in Service.objects.all():
        services.append({
            'id': service.id,
            'title': service.title,
            'image': service.image.url,
            'isExclusive': service.isExclusive,
            'subservices': service.subservice_set.all()[:5]
        })
    return render(request, "emitr/index.html", {
        "ExclusiveServices": Service.objects.filter(isExclusive=True),
        'services': services,
    })


def contact_view(request):
    return render(request, 'emitr/contact.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("emitr:index"))
        else:
            messages.info(request, "Invalid credentials!")
            return HttpResponseRedirect(reverse("emitr:login"))

    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse("emitr:login"))
        
    return render(request, "emitr/login.html")


@login_required(login_url="emitr:login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("emitr:index"))


def service_fee_view(request, service_id):
    return render(request, 'emitr/service_fee.html', {
        'service': Service.objects.get(pk=service_id),
        'subservices': Service.objects.get(pk=service_id).subservice_set.all()
    })