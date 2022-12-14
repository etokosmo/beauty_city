from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ServiceCategory(models.Model):
    title = models.CharField(verbose_name="Название категории", max_length=200)


class Salon(models.Model):
    title = models.CharField(verbose_name="Название салона", max_length=200)
    address = models.CharField(verbose_name="Адрес салона", max_length=200)


class Service(models.Model):
    title = models.CharField(verbose_name="Название услуги", max_length=200)
    price = models.PositiveIntegerField(verbose_name="Стоимость услуги")
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория услуги",
    )


class Master(models.Model):
    first_name = models.CharField(verbose_name="Имя мастера", max_length=200)
    second_name = models.CharField(
        verbose_name="Фамилия мастера", max_length=200
    )
    service = models.ManyToManyField(
        Service, verbose_name="Услуги мастера", related_name="masters"
    )
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True)


class User(models.Model):
    first_name = models.CharField(verbose_name="Имя клиента", max_length=200)
    second_name = models.CharField(
        verbose_name="Фамилия клиента", max_length=200
    )
    phone_number = PhoneNumberField(verbose_name='Номер телефона клиента', region='RU')


class Timeslot(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, verbose_name='Салон')
    day = models.DateField(verbose_name='Дата записи')
    time = models.TimeField(verbose_name='Время записи')

