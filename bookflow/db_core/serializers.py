from rest_framework import serializers

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