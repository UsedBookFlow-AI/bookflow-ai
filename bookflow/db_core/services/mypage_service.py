from db_core.models import Institution, InventoryBook, BookSupplyTransaction
from django.contrib.auth.models import User

class MyPageService:
    @staticmethod
    def get_mypage_data(user_id):
        user = User.objects.get(username=user_id)
        institution = Institution.objects.get(user=user)

        """(1) 공급자로서 등록한 재고 및 수급 신청 내역 조회"""
        # 해당 기관이 등록한 모든 재고 도서
        inventory_books = InventoryBook.objects.filter(institution=institution)
        supply_list = []

        for book in inventory_books:
            tx_list = BookSupplyTransaction.objects.filter(book=book).select_related(
                "requester_institution"
            )

            supply_list.append({
                "book_id" : str(book.id),
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "category": book.category,
                "initial_stock": book.stock + sum([tx.requested_amount for tx in tx_list]),
                "current_stock": book.stock,
                "transactions": [
                    {
                        "requester_institution": tx.requester_institution.institution_name,
                        "requested_amount": tx.requested_amount,
                        "requester_contact": tx.requester_institution.contact,
                        "requested_at": tx.created_at
                    }
                    for tx in tx_list
                ]
            })


        """(2) 수급자로서 내가 신청한 내역 조회"""
        requested_list = BookSupplyTransaction.objects.filter(
            requester_institution = institution
        ).select_related("supplier_institution", "book")

        request_list = []

        for tx in requested_list:
            request_list.append({
                "book_title": tx.book.title,
                "book_author": tx.book.author,
                "book_genre": tx.book.genre,
                "supplier_institution": tx.supplier_institution.institution_name,
                "requested_amount": tx.requested_amount,
                "requested_at": tx.created_at,
            })



        """(3) 최종 조합"""
        return {
            "institution_name": institution.institution_name,
            "as_supplier": supply_list,
            "as_requester": request_list
        }