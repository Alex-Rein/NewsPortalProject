import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_delete, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import mail_managers

from .models import PostCategory, Post
from .tasks import send_new_post_notification


# def send_notifications(preview, pk, title, subscribers):
#     send_new_post_notification.delay(post_id=pk)


# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        # send_new_post_notification.delay(post_id=instance.pk)  # debug
        pass


# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers_emails = []
#
#         for cat in categories:
#             subscribers = cat.subscribers.all()
#             subscribers_emails += [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)


@receiver(post_delete, sender=Post)
def notify_on_post_delete(sender, instance, **kwargs):
    mail_managers(
        subject=f'{instance.author.user.username} удалил пост',
        message=f'Пост с заголовком \n"{instance.title}"\n был удалён.'
    )

# """Первый вариант ограничения на посты с получением страницы с ошибкой"""
# @receiver(pre_save, sender=Post)
# def author_post_limit(sender, instance, **kwargs):
#     today = datetime.date.today()
#     post_limit = Post.objects.filter(author=instance.author, post_time__date=today).count()
#     if post_limit >= 3:
#         raise ValidationError('Ограничение на три поста в сутки.')
