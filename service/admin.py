from django.contrib import admin
from django.utils.html import format_html

from .models import ServiceCategory, Salon, Service, Master, User, Timeslot


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'second_name',
        'get_image_preview',
    ]
    readonly_fields = [
        'get_image_preview',
    ]
    def get_image_preview(self, obj):
        if not obj.image:
            return 'нет картинки'
        return format_html('<img src="{url}" style="max-height: 100px;"/>',
                           url=obj.image.url)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'second_name',
        'get_image_preview',
    ]

    readonly_fields = [
        'get_image_preview',
    ]
    def get_image_preview(self, obj):
        if not obj.image:
            return 'нет картинки'
        return format_html('<img src="{url}" style="max-height: 100px;"/>',
                           url=obj.image.url)


@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    pass
