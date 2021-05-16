import uuid

from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    name = models.CharField(
        _('full name'),
        max_length = 100,
        help_text = _(
            "Name of our registered user."
        )
    )
    phone = models.CharField(
        _('phone number'),
        max_length = 20,
        primary_key = True,
        help_text = _(
            "Phone number of our registered user."
        )
    )
    email = models.CharField(
        _('email id'),
        max_length = 100,
        null = True,
        blank = True,
        help_text = _(
            "Email ID of our registered user. ( Optional )"
        )
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user'

    def __str__(self):
        return self.name + " - " + self.phone


class GlobalDatabase(models.Model):
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False
    )
    name = models.CharField(
        _('full name'),
        max_length = 100,
        null = True,
        blank = True,
        help_text = _(
            "Name of the person."
        )
    )
    phone = models.CharField(
        _('phone number'),
        max_length = 20,
        help_text = _(
            "Phone number of the person."
        )
    )
    email = models.CharField(
        _('email id'),
        max_length = 100,
        null = True,
        blank = True,
        help_text = _(
            "Email ID of our registered user. ( Optional )"
        )
    )
    spam_status = models.BooleanField( 
        default = False,
        help_text = _(
            "True means person is spammer, Default False."
        )   
    )
    registration_status = models.BooleanField( 
        default = False,
        help_text = _(
            "True means person is a registered user. Default False."
        )   
    )
    user = models.ForeignKey(
        User,
        null = True,
        blank = True,
        related_name = 'contacts',
        on_delete = models.PROTECT,
        help_text = _(
            "Tells the particular user is linked to which registered USER -> whose CONTACT is this person."
        )
    )

    def __str__(self):
        return self.name + " - " + str(self.id)