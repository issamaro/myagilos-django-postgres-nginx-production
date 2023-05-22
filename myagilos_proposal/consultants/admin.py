from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Cases
from .models import Certifications
from .models import Certification_progress
from .models import Certification_targets
from .models import Consultants
from .models import Consultant_certifications
from .models import ForgotPassword

# Define CaseAdmin with readonly_fields for gpt_content and created_at, and empty_value_display set to "-empty-"
@admin.register(Cases)
class CaseAdmin(admin.ModelAdmin):
    readonly_fields = ["gpt_content", "created_at"]


# Register Certifications and Certification_progress models
@admin.register(Certifications)
class certificationsAdmin(admin.ModelAdmin):
    list_filter = ["company"]

@admin.register(Certification_progress)
class certification_progressAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in Certification_progress._meta.fields if f.name != "id"]
    list_filter = ["target__certification__company"]
    
    
# Define Certification_targetsAdmin with readonly_fields for target_year and semester
@admin.register(Certification_targets)
class certification_targetsAdmin(admin.ModelAdmin):
    readonly_fields = ["active", "target_year", "semester"]
    list_filter = ["certification__company", "target_year"]

# Define consultantsAdmin with readonly_fields for target
@admin.register(Consultants)
class consultantsAdmin(admin.ModelAdmin):
    readonly_fields = ["target"]
    search_fields = ("last_name__startswith", )

# Define consultant_certificationsAdmin with readonly_fields for created_at
@admin.register(Consultant_certifications)
class consultant_certificationsAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]
    list_filter = ["certification__company", "consultant"]

    
# Define CustomUserAdmin with readonly_fields for date_joined and last_login
class CustomUserAdmin(UserAdmin):
    readonly_fields = ["date_joined", "last_login"]

@admin.register(ForgotPassword)
class ForgotPasswordAdmin(admin.ModelAdmin):
    readonly_fields = ["username", "email", "salt_and_hash", "created_at", "expires_at", "active"]
    list_filter = ["username"]

# Unregister the default UserAdmin and register CustomUserAdmin instead
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
