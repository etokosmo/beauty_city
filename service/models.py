from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class ServiceCategory(models.Model):
    title = models.CharField(
        verbose_name="Название категории",
        max_length=200
    )

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'

    def __str__(self):
        return self.title


class Salon(models.Model):
    title = models.CharField(
        verbose_name="Название салона",
        max_length=200
    )
    address = models.CharField(
        verbose_name="Адрес салона",
        max_length=200
    )
    image = models.ImageField(verbose_name='Аватарка салона', blank=True,
                              null=True)

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(
        verbose_name="Название услуги",
        max_length=200
    )
    price = models.PositiveIntegerField(
        verbose_name="Стоимость услуги"
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория услуги",
        related_name='services'
    )

    image = models.ImageField(verbose_name='Аватарка салона', blank=True,
                              null=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class Master(models.Model):
    first_name = models.CharField(
        verbose_name="Имя мастера",
        max_length=200
    )
    second_name = models.CharField(
        verbose_name="Фамилия мастера",
        max_length=200
    )
    service = models.ManyToManyField(
        Service,
        verbose_name="Услуги мастера",
        related_name="masters"
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField(
        verbose_name="Аватарка",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.first_name


class User(models.Model):
    first_name = models.CharField(
        verbose_name="Имя клиента",
        max_length=200,
        default='undefined'
    )
    second_name = models.CharField(
        verbose_name="Фамилия клиента",
        max_length=200,
        default='username'
    )
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона клиента",
        region="RU",
        unique=True
    )
    passcode = models.PositiveIntegerField(
        verbose_name="Код проверки",
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name="Аватарка",
        default='acc.svg'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.phone_number}"

    def set_passcode(self):
        self.passcode = 7777
        # TODO create passcode logic


class Timeslot(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    master = models.ForeignKey(
        Master, on_delete=models.CASCADE,
        verbose_name='Мастер'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        verbose_name='Услуга'
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        verbose_name='Салон'
    )
    day = models.DateField(
        verbose_name='Дата записи'
    )
    time = models.TimeField(
        verbose_name='Время записи'
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f"{self.day}:{self.time}-{self.client}-{self.service}"


class Order(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        verbose_name='Услуга'
    )
    salon = models.ForeignKey(
        Salon, on_delete=models.CASCADE,
        verbose_name='Салон'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Создан в'
    )

    def __str__(self):
        return f"{self.client}-{self.salon}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        blank=True
    )
    master = models.ForeignKey(
        Master, on_delete=models.CASCADE,
        verbose_name='Мастер'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.user}:{self.text}"


class Document(models.Model):
    title = models.CharField(
        verbose_name="Название документа",
        max_length=200,
    )
    file = models.FileField(
        verbose_name="Файл"
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title
