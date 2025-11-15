from rest_framework import serializers
from django.contrib.auth.models import User
from db_core.models import Institution, InventoryBook, BookSupplyRequest

class RegisterUserSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    institution_name = serializers.CharField(max_length=255)
    is_supply_institution = serializers.BooleanField(default=False)
    is_procurement_institution = serializers.BooleanField(default=False)
    institution_address = serializers.CharField(max_length=255)
    contact = serializers.CharField(max_length=255)



class LoginUserSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)



class StoreInventoryBookSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=150)

    class Meta:
        model = InventoryBook
        fields = [
            'user_id',
            'title',
            'author',
            'category',
            'genre',
            'stock',
            'condition',
        ]

    def validate(self, data):
        # 기본 유효성 검증 로직
        if data.get('stock', 0) < 0:
            raise serializers.ValidationError({"stock": "재고 수량은 0 이상이어야 합니다."})

        valid_conditions = [choice[0] for choice in InventoryBook.CONDITION_CHOICES]
        if data.get('condition') not in valid_conditions:
            raise serializers.ValidationError({"condition": f"도서 상태는 {valid_conditions} 중 하나여야 합니다."})

        return data

    def create(self, validated_data):
        """
        user_id → Institution → InventoryBook 생성
        """
        user_id = validated_data.pop('user_id')
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "해당 사용자 ID가 존재하지 않습니다."})

        try:
            institution = Institution.objects.get(user=user)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({"institution": "해당 사용자에 연결된 기관이 존재하지 않습니다."})

        book = InventoryBook.objects.create(institution=institution, **validated_data)
        return book


class StoreBookSupplyRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=150)
    raw_request = serializers.CharField()

    def validate_raw_request(self, value):
        if not value.strip():
            raise serializers.ValidationError("요청 내용을 입력해주세요")
        return value