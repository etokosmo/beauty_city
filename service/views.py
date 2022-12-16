from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .auth_tools import get_user
from .forms import UserProfileForm
from .models import Salon, ServiceCategory, Master, Timeslot, Service, \
    Document, Comment


def service_page(request):
    user = get_user(request)
    salons = Salon.objects.all()
    categories = ServiceCategory.objects.prefetch_related('services')
    masters = Master.objects.all()
    privacy_file = get_object_or_404(Document, title='privacy_polite')

    context = {
        'client_info':
            {
                'first_name': user.first_name,
                'second_name': user.second_name,
                'image': user.image.url
            },
        'salons': [
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
        'client_info':
            {
                'first_name': user.first_name,
                'second_name': user.second_name,
                'image': user.image.url
            },
        'privacy_file': privacy_file,
        'client': user,
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

    order = {
        'client_info':
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

    order = {
        'client_info': {
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


def get_salons(request):
    salons = Salon.objects.all()
    data = serializers.serialize('json', salons)
    return HttpResponse(data, content_type='application/json')


def get_categories(request):
    categories = ServiceCategory.objects.all()
    if 'salon' in request.GET.keys():
        salon = request.GET['salon']
        categories = Salon.objects.filter(title=salon).first().categories.all()
    data = serializers.serialize('json', categories)
    return HttpResponse(data, content_type='application/json')


def get_services(request):
    services = Service.objects.all()
    if 'salon' in request.GET.keys():
        salon = request.GET['salon']
        categories = Salon.objects.filter(title=salon).first().categories.all()
        services = services.filter(category__in=categories)
    if 'category' in request.GET.keys():
        category = request.GET['category']
        services = services.filter(category__title=category)
    data = serializers.serialize('json', services)
    return HttpResponse(data, content_type='application/json')


def get_masters(request):
    masters = Master.objects.all()
    if 'salon' in request.GET.keys():
        salon = request.GET['salon']
        masters = masters.filter(salon__title=salon)
    if 'service' in request.GET.keys():
        service = request.GET['service']
        masters_id = Service.objects.filter(
            title=service).first().masters.values_list('id', flat=True)
        masters = masters.filter(id__in=masters_id)
    data = serializers.serialize('json', masters)
    return HttpResponse(data, content_type='application/json')


def profile_page(request):
    user = get_user(request)
    if not user:
        return render(request, 'index.html')
    form = UserProfileForm(
        request.POST or None,
        request.FILES or None,
        initial={
            "first_name": user.first_name,
            "second_name": user.second_name,
            "image": user.image
        })
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        second_name = form.cleaned_data.get("second_name")
        image = form.cleaned_data.get("image")

        user.first_name = first_name
        user.second_name = second_name
        user.image = image
        user.save()
        return redirect('service:note_page')

    context = {
        'client_info': {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': request.build_absolute_uri(user.image.url)
        },
        'form': form,
        'client': user
    }

    return render(request, 'profile.html', context=context)
