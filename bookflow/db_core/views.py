from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db_core.services.user_service import UserService
from db_core.services.stock_book_service import StockBookService
from db_core.services.book_supply_request_service import BookSupplyRequestService
from ai_engine.services.recsys_engine_service import RecsysEngineService
from db_core.serializers import RegisterUserSerializer, LoginUserSerializer, StoreInventoryBookSerializer, StoreBookSupplyRequestSerializer, InventoryBookResponseSerializer, BookSupplyApplySerializer
from django.contrib.auth.models import User

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserService.register_user(serializer.validated_data)
            return Response(
                {"message": "회원가입 성공", "user_id": user.username},
                status = status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        password = serializer.validated_data['password']

        try:
            user = UserService.authenticate_user(user_id, password)
            return Response(
                {"message": "로그인 성공", "status": "success", "user_id": user.username},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        

class StoreInventoryBookView(APIView):
    def post(self, request):
        serializer = StoreInventoryBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user_id = data.pop('user_id')

        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            return Response({"error": "해당 사용자 ID가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            book, status_flag = StockBookService.add_inventory_book(user, data)

            if status_flag == "updated": #기존 재고가 있을 시
                return Response({
                    "message": "기존 도서 재고가 증가했습니다.",
                    "book_id": str(book.id),
                    "title": book.title,
                    "new_stock": book.stock,
                    "institution": book.institution.institution_name
                }, status=status.HTTP_200_OK)

            return Response({ # 새 책 등록 시
                "message": "새 도서가 등록되었습니다.",
                "book_id": str(book.id),
                "title": book.title,
                "stock": book.stock,
                "institution": book.institution.institution_name
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class StoreBookSupplyRequestView(APIView):
    def post(self, request):
        serializer = StoreBookSupplyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        user=  User.objects.get(username=user_id)
        
        # book_request = BookSupplyRequestService.create_request(
        #     user=user,
        #     request_text=serializer.validated_data['raw_request']
        # )

        books = RecsysEngineService.route_answer(
            user=user,
            request_text=serializer.validated_data['raw_request']
        )
        print(books)

        books_serialized = InventoryBookResponseSerializer(books, many=True)

        return Response(
            {
                "message": "추천 도서 목록",
                "user_id" : user_id,
                "books" : books_serialized.data
            },
            status = 201
        )

class ApplyBookSupplyView(APIView):
    def post(self, request):
        serializer = BookSupplyApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            result = BookSupplyRequestService.apply_supply_request(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "서버 오류 발생", "detail": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(result, status=status.HTTP_201_CREATED)