from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .auth_tools import get_user
from .models import Salon, ServiceCategory, Master, Timeslot, Service, Comment, Document


def service_page(request):
    user = get_user(request)
    salons = Salon.objects.all()
    categories = ServiceCategory.objects.prefetch_related('services')
    masters = Master.objects.all()
    privacy_file = get_object_or_404(Document, title='privacy_polite')

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
        'client': user,
        'privacy_file': privacy_file,
    }

    return render(request, 'service.html', context)


def index_page(request):
    user = get_user(request)
    privacy_file = get_object_or_404(Document, title='privacy_polite')
    services = Service.objects.all()
    salons = Salon.objects.all()
    masters = Master.objects.all()
    comments = Comment.objects.all()

    context = {
        'privacy_file': privacy_file,
        'client':
        {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': user.image.url,
        },
        'services': [
            {
                'title': service.title,
                'price': service.price,
                'image': request.build_absolute_uri(service.image.url),
            }
            for service in services],

        'salons': [
            {
                'title': salon.title,
                'address': salon.address,
                'image': request.build_absolute_uri(salon.image.url),
            }
            for salon in salons],

        'masters': [
            {
                'first_name': master.first_name,
                'second_name': master.second_name,
                'salon': master.salon.title,
                'service': master.service.all()[0].title,
                'image': request.build_absolute_uri(
                    master.image.url),
                'comments': comments.filter(master=master.id).count(),
            }
            for master in masters],

        'comments': [
            {
                'user_first_name': comment.user.first_name,
                'user_second_name': comment.user.second_name,
                'text': comment.text,
                'master': comment.master,
            }
            for comment in comments],
    }
    return render(request, 'index.html', context)


def servicefinally_page(request):
    user = get_user(request)
    if not user:
        return render(request, 'index.html')
    timeslots = Timeslot.objects.filter(client=user.id).prefetch_related(
        'master').prefetch_related('service').prefetch_related('salon')

    order = {'client_info':
        {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': user.image.url
        },
        'timeslots': [
            {
                'id': timeslot.id,
                'master_first_name': timeslot.master.first_name,
                'master_second_name': timeslot.master.second_name,
                'master_image': request.build_absolute_uri(
                    timeslot.master.image.url),
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


def note_page(request):
    user = get_user(request)
    if not user:
        return render(request, 'index.html')
    timeslots = Timeslot.objects.filter(client=user.id).prefetch_related(
        'master').prefetch_related('service').prefetch_related('salon')

    order = {'client_info': {
        'first_name': user.first_name,
        'second_name': user.second_name,
        'image': request.build_absolute_uri(user.image.url)
    },
        'timeslots': [
            {
                'id': timeslot.id,
                'master_first_name': timeslot.master.first_name,
                'master_second_name': timeslot.master.second_name,
                'master_image': request.build_absolute_uri(
                    timeslot.master.image.url),
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
