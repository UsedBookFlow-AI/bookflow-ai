from django.contrib.auth.models import User
from db_core.models import Institution
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class UserService:
    @staticmethod
    def is_duplicate_user(user_id: str) -> bool:
        """user_id(username)이 이미 존재하는지 확인"""
        return User.objects.filter(username=user_id).exists()
    
    @staticmethod
    @transaction.atomic
    def register_user(data:dict) -> User:
        user_id = data['user_id']
        password = data['password']
        username = data ['username']
        contact = data['contact']

        if UserService.is_duplicate_user(user_id):
            raise ValueError('존재하는 회원입니다.')
        
        user = User.objects.create_user(username=user_id, password=password, first_name=username)
        user.date_joined = timezone.now()
        user.save()

        Institution.objects.create(
            user=user,
            institution_name = data['institution_name'],
            is_supply_institution = data.get('is_supply_institution', False),
            is_procurement_institution = data.get('is_procurement_institution', False),
            institution_address = data['institution_address'],
            contact=contact
        )

        return user