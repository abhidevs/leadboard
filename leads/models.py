from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class Organisation(models.Model):
    org_name = models.CharField(max_length=50)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.org_name


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30) # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        org_name = f"{instance.first_name} {instance.last_name}"
        Organisation.objects.create(org_name=org_name, admin=instance)


post_save.connect(post_user_created_signal, sender=User)