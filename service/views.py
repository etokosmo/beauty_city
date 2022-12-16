from django.shortcuts import render

from service.models import Salon, ServiceCategory, Master, Timeslot, User


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


def servicefinally_page(request, id=3):
    timeslots = Timeslot.objects.filter(client=id).prefetch_related(
        'master').prefetch_related('service').prefetch_related('salon')
    client = User.objects.get(id=id)

    order = {'client_info':
                {
                'first_name': client.first_name,
                'second_name': client.second_name,
                'image': client.image.url
                },
            'timeslots': [
                {
                    'id': timeslot.id,
                    'master_first_name': timeslot.master.first_name,
                    'master_second_name': timeslot.master.second_name,
                    'master_image': request.build_absolute_uri(timeslot.master.image.url),
                    'salon': timeslot.salon.title,
                    'salon_address': timeslot.salon.address,
                    'service_title': timeslot.service.title,
                    'service_price': timeslot.service.price,
                    'day': timeslot.day,
                    'time': timeslot.time
                }
            for timeslot in timeslots],

    }

    return render(request, 'serviceFinally.html', context=order)


def note_page(request, id=5):
    timeslots = Timeslot.objects.filter(client=id).prefetch_related(
        'master').prefetch_related('service').prefetch_related('salon')
    client = User.objects.get(id=id)

    order = {'client_info':
                {
                'first_name': client.first_name,
                'second_name': client.second_name,
                'image': request.build_absolute_uri(client.image.url)
                },
            'timeslots': [
                {
                    'id': timeslot.id,
                    'master_first_name': timeslot.master.first_name,
                    'master_second_name': timeslot.master.second_name,
                    'master_image': request.build_absolute_uri(timeslot.master.image.url),
                    'salon': timeslot.salon.title,
                    'salon_address': timeslot.salon.address,
                    'service_title': timeslot.service.title,
                    'service_price': timeslot.service.price,
                    'day': timeslot.day,
                    'time': timeslot.time
                }
            for timeslot in timeslots],

    }

    return render(request, 'notes.html', context=order)