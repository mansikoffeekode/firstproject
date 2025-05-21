from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.


# class TimeAt(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, name, password):
        if not email:
            raise ValueError("Users must have an email!")

        user = self.model(email=self.normalize_email(email),
                          name=name,
                          password=password)

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=self.normalize_email(email),
                          password=password)

        if password:
            user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=99, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{}-{}'.format(self.pk, self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
