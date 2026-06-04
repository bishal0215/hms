from django.contrib.auth.models import Permission, User
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='roles',
        help_text='Django permissions assigned to this role.',
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
