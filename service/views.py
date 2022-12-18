import datetime
import json

import stripe
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt

from .auth_tools import get_user
from .forms import UserProfileForm
from .models import Salon, ServiceCategory, Master, Timeslot, Service, \
    Document, Comment, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


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
                'salons': [master.title for master in master.salon.all()],
                'services': [master.title for master in master.service.all()],
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
        'client': user,
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
    orders_for_pay = []
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
                orders_for_pay.append(order.id)
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
        'order_sum': order_sum,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'orders_for_pay': orders_for_pay,
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


@csrf_exempt
def get_order(request):
    response = json.loads(request.body)['service_price']
    decoded_response = eval(response)
    order = {
        'price': decoded_response.get('service_price'),
        'order_id': decoded_response.get('id')
    }
    return JsonResponse(order)


def get_payment(request):
    if request.method == 'POST':
        response = request.POST
        order_id = response.get('order_id')
        try:
            order_id = int(order_id)
            order_ids = None
        except ValueError:
            order_ids = order_id
        try:
            price = int(response.get('price'))
            card_number = int(response.get('number').replace(" ", ""))
            card_cvc = int(response.get('cvc'))
            card_mm = int(response.get('mm'))
            card_gg = int(response.get('gg'))
        except TypeError:
            return redirect('service:note_page')
        card_owner = response.get('fname')
        email = response.get('email')
        line_items = []
        if order_ids:
            for order_id in order_ids.split(','):
                order = get_object_or_404(Order, id=order_id)
                line_items.append(
                    {
                        'price_data': {
                            'currency': 'rub',
                            'product_data': {
                                'name': order.service,
                            },
                            'unit_amount': order.service.price * 100,
                        },
                        'quantity': 1,
                    }
                )
        else:
            order = Order.objects.get(id=order_id)
            reference_id = order.id
            line_items.append(
                {
                    'price_data': {
                        'currency': 'rub',
                        'product_data': {
                            'name': order.service,
                        },
                        'unit_amount': price * 100,
                    },
                    'quantity': 1,
                }
            )

        payment = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": card_mm,
                "exp_year": card_gg,
                "cvc": card_cvc,
            },
            billing_details={
                "address": {
                    "country": 'RU',
                },
                "email": email if email else 'a@a.com',
                "name": card_owner,
            },
        )
        customer = stripe.Customer.create(
            payment_method=payment.id,
            email=email if email else 'a@a.com',
            name=card_owner,
        )
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            customer=customer.id,
            client_reference_id=order_ids if order_ids else reference_id,
            success_url=request.build_absolute_uri(reverse(
                'service:success')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('service:cancel')),
        )
        context = {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'session_id': session.stripe_id
        }
        return render(request, 'stripe.html', context=context)


def create_order(request):
    user = get_user(request)
    if not user:
        return render(request, 'index.html')
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


def success(request):
    session_id = request.GET.get('session_id')

    if session_id is None:
        return HttpResponseNotFound()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    reference_id = session.client_reference_id
    try:
        order_id = int(reference_id)
        order = get_object_or_404(
            Order,
            id=order_id
        )
        order.payment = True
        order.save()
    except ValueError:
        order_ids = reference_id.split(',')
        for order_id in order_ids:
            order = get_object_or_404(
                Order,
                id=order_id
            )
            order.payment = True
            order.save()
    return redirect('service:note_page')


def cancel(request):
    user = get_user(request)
    if not user:
        return render(request, 'index.html')
    context = {
        'client_info': {
            'first_name': user.first_name,
            'second_name': user.second_name,
            'image': request.build_absolute_uri(user.image.url)
        },
        'client': user
    }
    return render(request, 'cancel.html', context=context)
