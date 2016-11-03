from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

import os
from django.conf import settings

from tinymce.models import HTMLField

class AccountManager(BaseUserManager):
    """ Method for account model
    """
    def create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError("Users must have a valid email address.")
        if not kwargs.get("username"):
            raise ValueError("Users must have a valid username.")

        account = self.model(email=self.normalize_email(email), username=kwargs.get("username"))
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        """ method that creates a user that has Administrative
            access. (can access the admin panel)
        """
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True

        account.save()

        return account


class Account(AbstractBaseUser,PermissionsMixin):
    """ Custom model for the users. it extends to
        the `django.auth.models.User`
    """
    email = models.EmailField(_("Email"), max_length=225, unique=True)
    username = models.CharField(max_length=225, unique=True)
    full_name = models.CharField(_("Full name"), max_length=225, blank=True, null=True)

    section = models.ManyToManyField("Section", related_name="section")

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activated = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "{email}".format(email=self.email)

    def get_short_name(self):
        return "{}".format((self.email).split('@')[0])

    def email_as_username(self):
        """ extract username from email
        """
        return "{username}".format(username=self.email)


class Section(models.Model):
    """
    """
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_("Section Name"),max_length=225)

    email_cv = models.CharField(_("Cv email"), max_length=225, blank=True)
    full_name = models.CharField(_("Full name"), max_length=225, blank=True, null=True)
    phone = models.CharField(_("Phone number"),max_length=225, blank=True, null=True)
    website = models.CharField(_("Website"),max_length=225, blank=True, null=True)
    address_l1 = models.CharField(_("Address Line 1"),max_length=225, blank=True, null=True)
    address_l2 = models.CharField(_("Address Line 2"),max_length=225, blank=True, null=True)
    address_l3 = models.CharField(_("Address Line 3"),max_length=225, blank=True, null=True)
    photo = models.ImageField(upload_to='photo/', max_length=225, blank=True, null=True)

    reference = models.TextField(_("Reference"), blank=True, null=True)
    interest = models.TextField(_("Interest"), blank=True, null=True)
    qualification = models.TextField(_("Qualification"), blank=True, null=True)
    portfolio = models.TextField(_("Portfolio"), blank=True, null=True)
    # portfolio = HTMLField()

    def __str__(self):
        return "{}".format(self.name)

    def __init__(self, *args, **kwargs):
        super(Section, self).__init__(*args, **kwargs)
        self._photo = self.photo

    def save(self, *args, **kwargs):
        if self.photo != self._photo and self._photo != '':
            self.delete_photo()

        super(Section, self).save(*args, **kwargs)
        self._photo = self.photo

    def delete_photo(self, empty_photo=False):
        photo_path = os.path.join(settings.MEDIA_ROOT, str(self._photo))

        try:
            os.remove(photo_path)
        except Exception as e:
            pass

        if empty_photo:
            self.photo = ''


class Education(models.Model):
    """ Education attainment
    """
    section = models.ForeignKey("Section", blank=True)
    # section = models.ManyToManyField("Section", blank=True)
    course = models.CharField(_("Course name"), max_length=225, blank=True, null=True)
    institution = models.CharField(_("Institutions name"), max_length=225,blank=True, null=True)
    start = models.CharField(_("Start date"), max_length=225, blank=True, null=True)
    end = models.CharField(_("End date"), max_length=225, blank=True, null=True)
    other_information = models.TextField(_("Other informations"), blank=True, null=True)

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"


class Work(models.Model):
    """ Work experience
    """
    # section = models.ManyToManyField("Section", blank=True)
    section = models.ForeignKey("Section", blank=True)
    job = models.CharField(_("Job title"), max_length=225, blank=True, null=True)
    company = models.CharField(_("Company Name"), max_length=225, blank=True, null=True)
    start_work = models.CharField(_("Start date"), max_length=225, blank=True, null=True)
    end_work = models.CharField(_("End date"), max_length=225, blank=True, null=True)
    other_information_work = models.TextField(_("Other Informations"), blank=True, null=True)

    def __str__(self):
        return "{}".format(self.job)

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Works"



class SpecialSection(models.Model):

    """
    """
    section = models.ForeignKey("Section", blank=True)
    name = models.CharField(max_length=225)
    content = models.TextField(blank=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Special Section"
        verbose_name_plural = "Special Sections"