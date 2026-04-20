from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import SchoolUser

class SchoolUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolUser
        fields = ['id', 'email', 'school_name', 'school_type', 'region', 'district', 'phone', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = SchoolUser
        fields = ['email', 'school_name', 'school_type', 'region', 'district', 'phone', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = SchoolUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)