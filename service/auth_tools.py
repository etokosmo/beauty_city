import binascii
import hashlib
import hmac
import json
from base64 import b64encode, b64decode
from typing import Optional

from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

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


def set_passcode(request):
    response = json.loads(request.body)
    user_phone_number = response.get('tel')
    if not user_phone_number:
        return render(request, 'index.html')
    user, created = User.objects.get_or_create(
        phone_number=user_phone_number,
        passcode=7878
    )
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

def account(request):
    pass