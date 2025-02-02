from django.contrib import admin
from django.urls import path
from app.views import (
    RegisterView, 
    LoginView, 
    DashboardStudent, 
    DashboardParent, 
    DashboardSchool, 
    StudentAchievements,
    achievements,
    ForgotPasswordView,
    ResetPasswordConfirmView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication APIs
    path('api/auth/register/', RegisterView.as_view(), name="auth_register"),
    path('api/auth/login/', LoginView.as_view(), name="auth_login"),
    path('api/auth/forgot-password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('api/auth/reset-password/', ResetPasswordConfirmView.as_view(), name="reset_password"),
    
    # JWT Token APIs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Role-Based Dashboards
    path('api/dashboard/student/', DashboardStudent.as_view(), name='dashboard_student'),
    path('api/dashboard/parent/', DashboardParent.as_view(), name='dashboard_parent'),
    path('api/dashboard/school/', DashboardSchool.as_view(), name='dashboard_school'),

    # Student Achievements API (Only for Parents & Students)
    path('api/student/achievements/<int:student_id>/', StudentAchievements.as_view(), name='student_achievements'),
    path('api/achievements', achievements.as_view(), name='achievements'),
]