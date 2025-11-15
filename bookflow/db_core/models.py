# DB 스키마 정의 - ORM 클래스
import uuid
from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='institution')
    institution_name = models.CharField(max_length=255)
    is_supply_institution = models.BooleanField(default=False)
    is_procurement_institution = models.BooleanField(default=False)
    institution_address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.institution_name} ({self.user.username})"


class InventoryBook(models.Model):
    CONDITION_CHOICES = [
        ('새 책', '새 책'),
        ('양호', '양호'),
        ('손상', '손상'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name = 'books')
    title = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(default=0)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='양호')
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.title}] ({self.institution.institution_name})"
    


class BookSupplyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_request = models.TextField()
    target_age = models.CharField(max_length=50, null=True, blank=True)
    book_category = models.CharField(max_length=100, null=True, blank=True)
    book_amount = models.IntegerField(null=True, blank=True)
    others = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default = 'pending')
    created_at = models.DateTimeField(auto_now_add=True)
