from db_core.models import InstitutionUser
from django.core.exceptions import ObjectDoesNotExist

class UserService:
    @staticmethod
    def is_user_id_duplicate(user_id: str) -> bool:
        return InstitutionUser.objects.filter(user_id=user_id).exists()

    @staticmethod
    def register_user(data: dict) -> InstitutionUser:
        if UserService.is_user_id_duplicate(data['user_id']):
            raise ValueError("이미 존재하는 user_id입니다.")
        user = InstitutionUser.objects.create(**data)
        return user
