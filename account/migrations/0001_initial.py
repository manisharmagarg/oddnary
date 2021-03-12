# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-25 13:48
from __future__ import unicode_literals

import account.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.helper
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('oin', models.CharField(default=utils.helper.generate_oin, max_length=32, unique=True)),
                ('first_name', models.CharField(max_length=64, null=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=64, null=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['date_joined'],
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('organization', models.CharField(max_length=128, null=True)),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=64, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(max_length=64, null=True)),
                ('role', models.IntegerField(blank=True, choices=[(1, 'Subscriber'), (2, 'Instructor'), (3, 'Admin')], default=1)),
                ('avatar', models.ImageField(blank=True, help_text='max size should be 10 MB', max_length=1024, null=True, upload_to='avatars/', verbose_name='avatar')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_profile_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_profile_last_modified_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profile',
            },
        ),
        migrations.CreateModel(
            name='ProfileSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('dob_visible', models.BooleanField(default=False)),
                ('mobile_visible', models.BooleanField(default=False)),
                ('address_visible', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_profilesetting_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_profilesetting_last_modified_by', to=settings.AUTH_USER_MODEL)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='account.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]