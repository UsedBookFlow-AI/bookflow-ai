from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
        contact = data['contact']

        if UserService.is_duplicate_user(user_id):
            raise ValueError('존재하는 회원입니다.')
        
        user = User.objects.create_user(username=user_id, password=password)
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
    

    @staticmethod
    def authenticate_user(user_id, password) -> User:
        """아이디/비번 일치하는지 확인"""
        user = authenticate(username=user_id, password=password)
        if user is None:
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")
        return user