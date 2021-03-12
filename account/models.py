from uuid import uuid4

# Django imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

# Local imports
from .managers import UserManager
from utils.helper import generate_oin
from utils.constants import ROLES

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    oin = models.CharField(max_length=32, unique=True, default=generate_oin)
    first_name = models.CharField(_('first name'), max_length=64, blank=False, null=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=False, null=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['date_joined',]

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


# to avoid circular import
from utils.base_model import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=128, null=True, blank=False)
    mobile = models.CharField(max_length=15, null=True, blank=False)
    address = models.CharField(max_length=128, null=True, blank=False)
    city = models.CharField(max_length=64, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=False)
    role = models.IntegerField(choices=ROLES, blank=True, default=1)
    avatar = models.ImageField(_('avatar'), max_length=1024, upload_to="avatars/", 
                                null=True, blank=True,
                                help_text="max size should be 10 MB")

    class Meta():
        verbose_name = _('profile')
        verbose_name_plural = _('profile')

    def __str__(self):
        return '{}'.format(self.user)


class ProfileSetting(BaseModel):
    profile = models.OneToOneField(Profile, related_name='settings')
    dob_visible = models.BooleanField(default=False)
    mobile_visible = models.BooleanField(default=False)
    address_visible = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.profile)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            # admin
            Profile.objects.create(user=instance, role=3)
        else:
            #subscriber
            Profile.objects.create(user=instance, role=1)


@receiver(post_save, sender=Profile)
def initialize_profile_settings(sender, instance, created, *args, **kwargs):
    if created:
        ProfileSetting.objects.create(profile=instance)

