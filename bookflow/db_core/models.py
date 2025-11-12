# DB 스키마 정의 - ORM 클래스
import uuid
from django.db import models
from django.contrib.auth.models import User
from db_core.models import Institution

class Institution(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='institution')
    institution_name = models.CharField(max_length=255)
    is_supply_institution = models.BooleanField(default=False)
    is_procurement_institution = models.BooleanField(default=False)
    institution_address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.institution_name} ({self.user.username})"


