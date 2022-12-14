from django.shortcuts import render

def service_page(request):
    context = {}
    return render(request, 'service.html', context)

def index_page(request):
    context = {}
    return render(request, 'index.html', context)

