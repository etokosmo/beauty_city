import binascii
import hashlib
import hmac
import json
import random
from base64 import b64encode, b64decode
from typing import Optional
from urllib.parse import unquote

import requests
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from requests.exceptions import HTTPError, ConnectionError

from .models import User


def sign_data(data: str) -> str:
    """Возвращает подписанные data"""
    return hmac.new(
        settings.SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    if username_signed.count('.') != 1:
        return None
    username_base64, sign = username_signed.split('.')
    try:
        username = b64decode(username_base64.encode(), validate=True).decode()
    except binascii.Error:
        return None
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


def create_passcode() -> int:
    """Create random passcode"""
    return random.randint(1000, 9999)


def set_passcode(request):
    """Set passcode to User"""
    response = json.loads(request.body)
    user_phone_number = unquote(response.get('tel'))

    if not user_phone_number:
        return render(request, 'index.html')

    _passcode = create_passcode()
    _token = settings.TELEGRAM_ACCESS_TOKEN
    _chat_id = settings.TELEGRAM_CHAT_ID

    user, created = User.objects.get_or_create(
        phone_number=user_phone_number,
    )

    message = f"Пароль для пользователя {user_phone_number}:\n{_passcode}"

    user.passcode = _passcode
    user.save()

    url = f"https://api.telegram.org/bot{_token}/sendMessage?chat_id={_chat_id}&text={message}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError:
        pass
        # TODO create failed log
    except ConnectionError:
        pass
        # TODO create failed log

    context = {'client': user}
    response = render(request, 'index.html', context)
    response.set_cookie('user_id', user.pk)
    return response


def verify_user(request):
    response = json.loads(request.body)
    user_passcode = int(response.get('passcode'))
    user_id = request.COOKIES.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    user_phone_number = f"{user.phone_number}"
    if user.passcode == user_passcode:
        user_signed = b64encode(
            user_phone_number.encode()).decode() + '.' + sign_data(
            user_phone_number)

        response_data = {
            'result': 'success',
            'user_phone_number': user_signed
        }
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

    response_data = {
        'result': 'failed',
        'user_phone_number': ''
    }
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


def logout_user(request):
    response = redirect('service:index_page')
    response.delete_cookie('user_phone_number')
    return response


def get_user(request) -> Optional[User]:
    user_phone_number = request.COOKIES.get('user_phone_number')
    if user_phone_number is None:
        return None

    valid_user_phone_number = get_username_from_signed_string(
        user_phone_number)

    if not valid_user_phone_number:
        return None
    try:
        user = User.objects.get(phone_number=valid_user_phone_number)
        return user
    except User.DoesNotExist:
        return None

