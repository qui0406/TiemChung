from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
import uuid
from django.utils import timezone

from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from rest_framework.authtoken.models import Token
from django.conf import settings



class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    ADMIN = 'admin'
    EMPLOYER = 'employer'
    CANDIDATE = 'candidate'
    ROLE_CHOICES = (
        (ADMIN, 'Quản trị viên'),
        (EMPLOYER, 'Nhà tuyển dụng'),
        (CANDIDATE, 'Ứng viên'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)
    email = models.EmailField(unique=True, null=True, blank=True)
    avatar = CloudinaryField(null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # Xac thuc nguoi dung

    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# class VaccineType(BaseModel):
#     name = models.CharField(_('name'), max_length=50, unique=True)

#     def __str__(self):
#         return self.name

# def get_default_vaccine_type():
#     return VaccineType.objects.get(name='COVID-19').id

# class Vaccine(BaseModel):
#     class Status(models.TextChoices):
#         ACTIVE = 'Active', _('Dang su dung')
#         DISCONTINUED = 'Discontinued', _('Ngung su dung')
#         PENDING_APPROVAL = 'Pending Approval', _('Chua phe duyet')
#         EXPIRED = 'Expired', _('Da het han')

#     name = models.CharField(max_length=100,verbose_name=_('Ten Vaccine'))
#     image = models.ImageField(upload_to='vaccines',blank=True, null=True)
#     vaccine_type = models.ForeignKey(VaccineType, on_delete=models.CASCADE,default=get_default_vaccine_type)
#     manufacturer = models.CharField(max_length=100, blank=True, null=True)
#     dose_count = models.IntegerField(default=10000)
#     dose_interval = models.CharField(max_length=50, blank=True, null=True)
#     age_group = models.CharField(max_length=50, blank=True, null=True)
#     description = RichTextField(blank=True, null=True)
#     approved_date = models.DateField(blank=True, null=True)
#     status = models.CharField(
#         max_length=20,
#         choices=Status.choices,
#         default=Status.ACTIVE
#     )

#     class Meta:
#         unique_together = (('name', 'vaccine_type'),)

#     def __str__(self):
#         return self.name

# class InjectionSite(BaseModel):
#     name = models.CharField(max_length=100)
#     address = models.TextField()
#     phone = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return self.name

# class InjectionSchedule(BaseModel):
#     vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
#     site = models.ForeignKey(InjectionSite, on_delete=models.CASCADE)
#     date = models.DateField()
#     slot_count = models.PositiveIntegerField(default=100)

#     def __str__(self):
#         return f"{self.vaccine.name} - {self.date}"


# class Appointment(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     schedule = models.ForeignKey(InjectionSchedule, on_delete=models.CASCADE)
#     registered_at = models.DateTimeField(auto_now_add=True)
#     is_confirmed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.username} - {self.schedule}"

# class VaccinationRecord(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     vaccine = models.ForeignKey(Vaccine, on_delete=models.SET_NULL, null=True)
#     dose_number = models.PositiveIntegerField()
#     injection_date = models.DateField()
#     site = models.ForeignKey(InjectionSite, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.vaccine.name} - Dose {self.dose_number}"
