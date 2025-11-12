from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db_core.services.user_service import UserService
from db_core.serializers import RegisterUserSerializer, LoginUserSerializer

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