from django.contrib import admin
from .models import Role, UserRole, StudentProfile, Achievements

admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(StudentProfile)
admin.site.register(Achievements)
