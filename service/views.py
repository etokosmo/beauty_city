from django.shortcuts import render

from service.models import Salon, ServiceCategory, Master


def service_page(request):
    salons = Salon.objects.all()
    categories = ServiceCategory.objects.prefetch_related('services')
    masters = Master.objects.all()

    context = {'salons': [
        {
            'title': salon.title,
            'address': salon.address,
            'image': salon.image
        }
        for salon in salons],
        'categories': [
            {
                'title': category.title,
                'services': category.services.all,
            }
            for category in categories],
        'masters': [
            {
                'first_name': master.first_name,
                'second_name': master.second_name,

            }
            for master in masters],
    }

    return render(request, 'service.html', context)


def index_page(request):
    context = {}
    return render(request, 'index.html', context)
