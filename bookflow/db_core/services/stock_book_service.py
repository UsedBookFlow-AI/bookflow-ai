from db_core.models import InventoryBook, Institution
from django.contrib.auth.models import User


class StockBookService:
    @staticmethod
    def add_inventory_book(user_id, data):
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            raise ValueError("해당 사용자 ID가 존재하지 않습니다.")

        try:
            institution = Institution.objects.get(user=user)
        except Institution.DoesNotExist:
            raise ValueError("기관 정보가 존재하지 않습니다.")

        book = InventoryBook.objects.create(
            institution=institution,
            title=data['title'],
            author=data.get('author', ''),
            category=data.get('category', ''),
            stock=data.get('stock', 0),
            condition=data.get('condition', '양호')
        )

        return book