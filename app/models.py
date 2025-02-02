from django.db import models
from django.contrib.auth.models import User
import bcrypt
from django.contrib.auth.tokens import default_token_generator





class Role(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name





# User.............................................................................................


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')




# Student ......................................................................................

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    school = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    




# Achievements........................................................................

class Achievements(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.TextField()

    def __str__(self):
        return f"{self.student.user.username} - {self.achievement}"





# Password Hashing using bcrypt................................................................................

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))





# Forgot Password Functionality
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return default_token_generator.check_token(self.user, self.token)
