import pytz
from datetime import *

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Subscription


@shared_task
def send_update_course_mail(course_id):
    """
    Отправляет электронное письмо подписчикам, если курс был обновлен не более 4 часов назад.
    """
    subscriptions = Subscription.objects.filter(course_id=course_id, active=True)

    for subscription in subscriptions:

        if (subscription.active
                and subscription.course.last_update < datetime.now(pytz.timezone(settings.TIME_ZONE))
                + timedelta(hours=4)):
            send_mail(
                subject=f"Курс '{subscription.course.title}' был обновлен.",
                message=f"В программе курса '{subscription.course.title}' произошли изменения.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
            )
