from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class Users(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=40, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    citiy = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payments(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Ученик', related_name="user_payment", **NULLABLE)
    date_of_payment = models.DateField(verbose_name='Дата оплаты', auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, verbose_name='Способ оплаты')
    id_session = models.CharField(max_length=255, verbose_name='id сессии', help_text='Укажите id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='ссылка на оплату', help_text='Укажите ссылку на оплату', **NULLABLE)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return (
            f"{self.user}: {self.date_of_payment}, {self.payment_amount}, {self.payment_method}, "
            f"за {self.paid_course if self.paid_course else self.paid_lesson}")
