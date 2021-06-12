from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    User_Type = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('vendor', 'Vendor'),
        ('user', 'User'),
    ]
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(choices=User_Type, default='user', max_length=50)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.user_type == 'user':
            return str(self.clientuserser.first_name) + " " + str(self.clientuserser.last_name)
        elif self.user_type == 'vendor':
            return str(self.vendor.company_name)
        else:
            return None


class ClientUser(models.Model):
    user = models.OneToOneField(User, verbose_name="Client User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Client User"
        verbose_name_plural = "Client Users"

    def get_client_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.user.email


class Vendor(models.Model):
    user = models.OneToOneField(User, verbose_name="Vendor User", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    registration_certificate = models.ImageField(upload_to="vendor_certificate", null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)
    geom = models.PointField(srid=4326, null=True, blank=True)

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_other_user(sender, instance, created, **kwargs):
    if created:
        u_id = instance.id
        if instance.user_type == 'user':
            user = ClientUser(user_id=u_id)
            user.save()
        elif instance.user_type == 'vendor':
            user = Vendor(user_id=u_id)
            user.save()
        else:
            pass
    else:
        pass
