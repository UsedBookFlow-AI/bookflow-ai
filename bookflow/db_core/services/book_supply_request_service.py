from db_core.models import BookSupplyRequest, Institution, InventoryBook, BookSupplyTransaction
from django.contrib.auth.models import User
from django.db import transaction

class BookSupplyRequestService:
    @staticmethod
    def create_request(user, request_text):
        return BookSupplyRequest.objects.create(
            user = user,
            raw_request = request_text,
            status = 'pending'
        )
    
    @staticmethod
    def update_request_info(request_id, extracted):
        req = BookSupplyRequest.objects.get(id=request_id)
        req.target_age = extracted.get('target_age')
        req.book_category = extracted.get('book_category')
        req.book_amount = extracted.get('book_amount')
        req.others = extracted.get('others')
        req.status = 'parsed'
        req.save()
        return req
    
    @staticmethod
    @transaction.atomic
    def apply_supply_request(data):
        user = User.objects.get(id=data['user_id'])
        requester_inst = Institution.objects.get(user_id=user)
        supplier_inst = Institution.objects.get(id=data['institution_id'])
        book = InventoryBook.objects.select_for_update().get(id=data['book_id'], institution=supplier_inst)
        req_amount = int(data['request_stock'])

        if book.stock < req_amount:
            raise ValueError('재고가 부족합니다.')
        
        #재고 차감
        book.stock -= req_amount
        book.save()

        #신청 기록 생성
        transaction = BookSupplyTransaction.objects.create(
            requester_institution = requester_inst,
            supplier_institution = supplier_inst,
            book=book,
            requested_amount=req_amount,
            status='completed'
        )

        return {
            "message": "신청 완료",
            "transaction_id": transaction.id,
            "book_title": book.title,
            "requested_amount": req_amount,
            "supplier_institution": supplier_inst.institution_name,
            "requester_institution": requester_inst.institution_name
        }