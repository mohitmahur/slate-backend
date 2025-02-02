from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, UserRole, StudentProfile, Achievements






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')




class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)
    school = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'school')

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        school_name = validated_data.pop('school', None)

        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )

        if role_name:
            role, created = Role.objects.get_or_create(name=role_name)
            UserRole.objects.create(user=user, role=role)

            if role_name == 'student' and school_name:
                StudentProfile.objects.create(user=user, school=school_name)

        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)




class AchievementSerializer(serializers.ModelSerializer):
    student=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Achievements
        fields = ('student', 'achievement')
