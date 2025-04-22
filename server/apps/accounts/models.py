from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from apps.accounts.managers import CustomUserManager

from apps.common.models import IsDeletedModel


class User(PermissionsMixin,AbstractBaseUser,IsDeletedModel):
    """
    Custom user model extending AbstractBaseUser
    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (EmailField): The email address of the user, used as the username field.
        avatar (ImageField): The avatar image of the user.
        is_staff (bool): Designates whether the user can log into this admin site.
        is_active (bool): Designates whether this user should be treated as active.
        account_type (str): The type of account (SELLER or BUYER).

    Methods:
        full_name(): Returns the full name of the user.
        __str__(): Returns the string representation of the user.

    """
    ACCOUNT_TYPE=(
        ('SELLER','SELLER'),
        ('BUYER','BUYER'),
    )
    first_name = models.CharField(max_length=30,verbose_name='Имя',null=True)
    last_name = models.CharField(max_length=30,verbose_name='Фамилия',null=True)
    email = models.EmailField(unique=True,verbose_name='Электронная почта')
    avatar=models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/%Y/%m/%d',
        blank=True,
        default='avatars/default.png',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    is_staff = models.BooleanField(default=False,verbose_name='Сотрудник')
    is_active = models.BooleanField(default=True,verbose_name='Активен')
    account_type=models.CharField(
        choices=ACCOUNT_TYPE,
        max_length=6,
        default='BUYER',
        verbose_name='Тип пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    @property
    def full_name(self):
        """return full name"""
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """string representation of user(full name + email)"""
        return f'{self.full_name}-{self.email}'






