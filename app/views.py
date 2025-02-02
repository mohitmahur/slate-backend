from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import StudentProfile, Achievements, PasswordResetToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, AchievementSerializer, PasswordResetSerializer, ResetPasswordConfirmSerializer
from .permissions import HasRole


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        return Response({'detail': 'Invalid Credentials'}, status=401)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = get_random_string(50)
                PasswordResetToken.objects.create(user=user, token=token)
                reset_link = f"http://localhost:8000/api/auth/reset-password/?token={token}"
                send_mail("Password Reset", f"Click the link to reset your password: {reset_link}", "admin@example.com", [email])
            return Response({"message": "If your email exists, a password reset link has been sent."})
        return Response(serializer.errors, status=400)


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password has been successfully reset."})
        return Response(serializer.errors, status=400)


# Student Dashboard/........................................................................................
class DashboardStudent(APIView):
    permission_classes = [IsAuthenticated, HasRole]
    required_role = 'student'

    def get(self, request):
        user = request.user
        student_profile = get_object_or_404(StudentProfile, user=user)
        achievements = Achievements.objects.filter(student=student_profile)
        achievements_serializer = AchievementSerializer(achievements, many=True)

        return Response({
            'message': 'Welcome to Student Dashboard',
            'user': UserSerializer(user).data,
            'achievements': achievements_serializer.data
        }, 200)


# DashboardParent.............................................................................................

class DashboardParent(APIView):
    permission_classes = [IsAuthenticated, HasRole]
    required_role = 'parent'

    def get(self, request):
        user = request.user
        linked_student = get_object_or_404(StudentProfile, user__id=request.user.id)
        achievements = Achievements.objects.filter(student=linked_student)
        achievements_serializer = AchievementSerializer(achievements, many=True)

        return Response({
            'message': 'Welcome to Parent Dashboard',
            'user': UserSerializer(user).data,
            'child_achievements': achievements_serializer.data
        }, 200)


# DashboardSchool/................................................................................................

class DashboardSchool(APIView):
    permission_classes = [IsAuthenticated, HasRole]
    required_role = 'school'

    def get(self, request):
        user = request.user
        students = StudentProfile.objects.all()
        student_serializer = UserSerializer([s.user for s in students], many=True)

        return Response({
            'message': 'Welcome to School Dashboard',
            'students': student_serializer.data
        }, 200)


# Achievements...................................................................................................

class StudentAchievements(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        user = request.user
        student_profile = get_object_or_404(StudentProfile, id=student_id)
        
        if not (user.user_roles.filter(role__name="parent") or user.user_roles.filter(role__name="student")):
            return Response({"error": "Unauthorized"}, status=403)

        achievements = Achievements.objects.filter(student=student_profile)
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data, 200)


# Creating Achievements................................................................................

class achievements(generics.ListCreateAPIView):
    queryset = Achievements.objects.all
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)