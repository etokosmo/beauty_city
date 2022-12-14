from django.contrib import admin

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
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    pass
