from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from db_core.services.user_service import UserService

@csrf_exempt
def register_user_view(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST 요청만 가능합니다."}, status=405)

    try:
        data = json.loads(request.body)
        user = UserService.register_user(data)
        return JsonResponse({"message": "회원가입 성공", "user_id": user.username}, status=201)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)