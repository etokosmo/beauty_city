from django.contrib import admin
from django.utils.html import format_html

from .models import ServiceCategory, Salon, Service, Master, User, Timeslot, \
    Order, Comment


def get_image_preview(self, obj):
    if not obj.image:
        return 'нет картинки'
    return format_html('<img src="{url}" style="max-height: 100px;"/>',
                       url=obj.image.url)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'master',
    ]

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    get_image_preview = get_image_preview

    list_display = [
        'title',
        'get_image_preview',
    ]
    readonly_fields = [
        'get_image_preview',
    ]


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    get_image_preview = get_image_preview

    list_display = [
        'first_name',
        'second_name',
        'get_image_preview',
    ]
    readonly_fields = [
        'get_image_preview',
    ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    get_image_preview = get_image_preview

    list_display = [
        'phone_number',
        'id',
        'first_name',
        'second_name',
        'get_image_preview',
    ]

    readonly_fields = [
        'get_image_preview',
    ]


@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'master',
        'salon',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'service',
        'salon',
    ]
