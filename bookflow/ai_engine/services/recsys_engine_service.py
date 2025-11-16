from db_core.models import BookSupplyRequest, InventoryBook
from django.contrib.auth.models import User

#TODO : 문장에 포함된 말에 따라 DB에서 해당 값들 가져오기
#값 : title, author, 출판사(institution_id 타고 들어가서 institution_name),category, stock
#ai 추천 이유는 내가 임의로 작성..? llm한테 추천 리스트를 보내주고 각각 추천하는 이유를 적어달라고 하기
class RecsysEngineService:
    @staticmethod
    def route_answer(user, request_text):
        POETRY_KEYWORDS = ["시", "시집", "시 작품", "시 모음"]

        if "어린이" in request_text or "아동" in request_text:
            books = (
                InventoryBook.objects
                .select_related("institution") #institution join
                .filter(category='아동·유아')
            )
            return books
        
        elif "경제경영" in request_text or "경제" in request_text or "경영" in request_text:
            books = (
                InventoryBook.objects
                .select_related("institution") #institution join
                .filter(category='경제·경영')
            )
            return books
        
        elif "한강" in request_text and '장편소설' in request_text:
            books = (
                InventoryBook.objects
                .select_related("institution")
                .filter(author='한강', genre='장편소설')
            )
            return books
        
        elif "한강" in request_text and any(k in request_text for k in POETRY_KEYWORDS):
            books = (
                InventoryBook.objects
                .select_related("institution")
                .filter(author='한강', genre='시')
            )
            return books
        
        else:
            books = (
                InventoryBook.objects
                .select_related('institution')
            )
            return books


