from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('SELLER', 'Seller'),
        ('ADMIN', 'Admin'),
    )

    SELLER_REQUEST_CHOICES = (
        ('NONE', 'None'),
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    seller_request_status = models.CharField(
        max_length=10,
        choices=SELLER_REQUEST_CHOICES,
        default='NONE'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email