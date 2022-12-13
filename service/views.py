from django.shortcuts import render

def service_page(request):
    context = {}
    return render(request, 'service.html', context)

