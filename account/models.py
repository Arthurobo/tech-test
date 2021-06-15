from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse

from multiselectfield import MultiSelectField
# from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first Name")
        if not last_name:
            raise ValueError("Users must have a Last Name")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.email) + "_" + "_" + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return "assets/defaultProfileImage/default.jpg"

class Account(PermissionsMixin, AbstractBaseUser):
    SEX_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female',),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, 
                                        null=True, blank=True, default='default.jpg')

    email = models.EmailField(verbose_name='email', max_length=50, unique=True)


    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=255)
    subjects_taught = models.CharField(max_length=255)

    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)

    
    
    # profile_picture = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, 
    #                                     null=True, blank=True, default='default.jpg')

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

 	# To be sure of admin permissions, NOTE: all admins have permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True  

    def get_absolute_url(self):
        return reverse('account:user-account-view', kwargs={'user_id': self.id})



class Profile(models.Model):

    SUBJECTS_TAUGHT_CHOICES = (
    ('1', 'English Language'),
    ('2', 'Mathematics'),
    ('3', 'Physics'),
    ('4', 'Biology'),
    ('5', 'Chemistry'),
    ('6', 'Agriculture'),
    ('7', 'History'),
)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects_taught = MultiSelectField(max_length=14,choices=SUBJECTS_TAUGHT_CHOICES, max_choices=5, blank=False,)
    room_number = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('account:account-detail-view', kwargs={'pk': self.user.pk})
        # Getting the slug of Account through 'self.user' as a foreignkey Note: To be used later
        # return reverse('account:account-detail-view', kwargs={'slug': self.user.slug}) 


def profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


post_save.connect(profile_receiver, sender=settings.AUTH_USER_MODEL)

