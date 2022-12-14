from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from scraping.models import City, Language


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return f'{self.user.username}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE, )
    notify = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        subscription = Subscription.objects.create(user=instance)
        Profile.objects.create(user=instance, subscription=subscription)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.subscription.save()
