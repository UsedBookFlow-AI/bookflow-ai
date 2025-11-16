from db_core.models import InventoryBook, Institution
from django.contrib.auth.models import User
from django.db import transaction


class StockBookService:
    # 1. User 조회
    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(username=user_id)
        except User.DoesNotExist:
            raise ValueError("해당 사용자 ID가 존재하지 않습니다.")


    # 2. Institution 조회
    @staticmethod
    def get_institution(user):
        try:
            return Institution.objects.get(user=user)
        except Institution.DoesNotExist:
            raise ValueError("기관 정보가 존재하지 않습니다.")


    # 3. 기존 책 존재 여부 조회
    @staticmethod
    def find_existing_book(institution, data):
        return InventoryBook.objects.filter(
            institution=institution,
            title=data.get("title"),
            author=data.get("author", ""),
        ).first()


    # 4. 기존 책 stock 증가
    @staticmethod
    def increase_stock(book, stock_to_add):
        book.stock += stock_to_add
        book.save()
        return book


    # 5. 새 책 생성
    @staticmethod
    def create_new_book(institution, data, stock_to_add):
        return InventoryBook.objects.create(
            institution=institution,
            title=data.get("title"),
            author=data.get("author", ""),
            category=data.get("category", ""),
            genre=data.get("genre", ""),
            stock=stock_to_add,
            condition=data.get("condition", "양호")
        )


    # 6. 메인 로직
    @staticmethod
    def add_inventory_book(user_id, data):

        user = StockBookService.get_user(user_id)
        institution = StockBookService.get_institution(user)

        stock_to_add = int(data.get("stock", 0))

        with transaction.atomic():
            existing_book = StockBookService.find_existing_book(institution, data)

            if existing_book:
                updated_book = StockBookService.increase_stock(existing_book, stock_to_add)
                return updated_book, "updated"
            
            new_book = StockBookService.create_new_book(institution, data, stock_to_add)
            return new_book, "new_book"
