from django.shortcuts import render

from .auth_tools import get_username_from_signed_string
from .models import Salon, ServiceCategory, Master, User


def service_page(request):
    user_phone_number = request.COOKIES.get('user_phone_number')
    context = {}
    if user_phone_number is None:
        return render(request, 'index.html', context)

    valid_user_phone_number = get_username_from_signed_string(
        user_phone_number)

    if not valid_user_phone_number:
        response = render(request, 'index.html', context)
        response.set_cookie('user_phone_number', None)
        return response
    try:
        user = User.objects.get(phone_number=valid_user_phone_number)
    except User.DoesNotExist:
        return render(request, 'index.html', context)

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
        'client': user
    }

    return render(request, 'service.html', context)


def index_page(request):
    user_phone_number = request.COOKIES.get('user_phone_number')
    context = {}
    if user_phone_number is None:
        return render(request, 'index.html', context)

    valid_user_phone_number = get_username_from_signed_string(
        user_phone_number)

    if not valid_user_phone_number:
        response = render(request, 'index.html', context)
        response.set_cookie('user_phone_number', None)
        return response
    try:
        user = User.objects.get(phone_number=valid_user_phone_number)
    except User.DoesNotExist:
        return render(request, 'index.html', context)
    context = {'client': user}
    return render(request, 'index.html', context)


def account(request):
    context = {}
    return render(request, 'notes.html', context)
