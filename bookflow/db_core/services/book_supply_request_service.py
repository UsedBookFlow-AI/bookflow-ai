from db_core.models import BookSupplyRequest
from django.contrib.auth.models import User

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