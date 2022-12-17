import datetime
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .auth_tools import get_user
from .forms import UserProfileForm
from .models import Salon, ServiceCategory, Master, Timeslot, Service, \
    Document, Comment, Order


def service_page(request):
    user = get_user(request)
    salons = Salon.objects.all()
    categories = ServiceCategory.objects.prefetch_related('services')
    masters = Master.objects.all()
    privacy_file = get_object_or_404(Document, title='privacy_polite')
    if user:
        client_info = {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': request.build_absolute_uri(user.image.url)
        }
    else:
        client_info = {
            'first_name': 'undefined',
            'second_name': 'username',
            'image': None
        }
    context = {
        'client_info': client_info,
        'salons': [
            {
                'title': salon.title,
                'address': salon.address,
                'image': request.build_absolute_uri(salon.image.url)
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
                'image': request.build_absolute_uri(master.image.url)

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

    if user:
        client_info = {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': user.image.url
        }
    else:
        client_info = {
            'first_name': 'undefined',
            'second_name': 'username',
            'image': None
        }

    context = {
        'client_info': client_info,
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


def get_order_date(orders_params):
    return orders_params['day']


def note_page(request):
    user = get_user(request)
    if not user:
        return render(request, 'index.html')
    orders = Order.objects.filter(client=user.id).prefetch_related(
        'master').prefetch_related('service').prefetch_related('salon')
    orders_params = []
    order_sum = 0
    for order in orders:
        if order.day >= datetime.date.today():
            order_item = {
                'id': order.id,
                'master_first_name': order.master.first_name,
                'master_second_name': order.master.second_name,
                'master_image': request.build_absolute_uri(
                    order.master.image.url),
                'salon': order.salon.title,
                'salon_address': order.salon.address,
                'service_title': order.service.title,
                'service_price': order.service.price,
                'day': order.day,
                'time': order.time,
                'payment': order.payment,
                'created_at': order.created_at,
                'new': True
            }
            orders_params.append(order_item)
            if not order.payment:
                order_sum += order.service.price
        else:
            order_item = {
                'id': order.id,
                'master_first_name': order.master.first_name,
                'master_second_name': order.master.second_name,
                'master_image': request.build_absolute_uri(
                    order.master.image.url),
                'salon': order.salon.title,
                'salon_address': order.salon.address,
                'service_title': order.service.title,
                'service_price': order.service.price,
                'day': order.day,
                'time': order.time,
                'payment': order.payment,
                'created_at': order.created_at,
                'new': False
            }
            orders_params.append(order_item)

    orders_params_sorted = sorted(orders_params,
                                  key=get_order_date)
    context = {
        'client_info': {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': request.build_absolute_uri(user.image.url)
        },
        'orders': orders_params_sorted,
        'order_sum': order_sum
    }

    return render(request, 'notes.html', context)


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


# def filling_master(apps, schema_editor):
#     Timeslot = apps.get_model('service', 'Timeslot')
#     Order = apps.get_model('service', 'Order')
#     for timeslot in Timeslot.objects.all().iterator():
#         order = Order.objects.get(id=timeslot.id)
#         order.master = timeslot.master
#         order.save()
#
# class Migration(migrations.Migration):
#
#     dependencies = [
#         ('service', '0015_order_master'),
#     ]
#
#     operations = [migrations.RunPython(filling_master)
#     ]


@csrf_exempt
def get_order(request):
    response = json.loads(request.body)['service_price']
    decoded_response = eval(response)
    order = {
        'price': decoded_response.get('service_price'),
        'order_id': decoded_response.get('id')
    }
    return JsonResponse(order)


@csrf_exempt
def get_payment(request):
    response = request.POST
    print(response)

    return JsonResponse({'order': 1})

def create_order(request):
    user = get_user(request)
    timeslots = Timeslot.objects.filter(client=user.id).prefetch_related(
        'master').prefetch_related('service').prefetch_related('salon')
    for timeslot in timeslots:
        Order.objects.get_or_create(
            id=timeslot.id,
            service=timeslot.service,
            client=timeslot.client,
            salon=timeslot.salon,
            day=timeslot.day,
            time=timeslot.time,
            payment=False,
            master=timeslot.master,
        )
    Timeslot.objects.all().delete()
    return redirect('service:note_page')
