from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from apps.users.models import Organization, SshPublicKey, GitHubOrganization

User = get_user_model()

class GitHubOrganizationInline(admin.TabularInline):
    model = GitHubOrganization
    extra = 1
    fields = ('login', 'github_org_id')
    readonly_fields = ('github_org_id',)
    can_delete = True
    show_change_link = False

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (GitHubOrganizationInline,)

class SshPublicKeyInline(admin.TabularInline):
    model = SshPublicKey
    extra = 1
    readonly_fields = ('fingerprint',)
    fields = ('name', 'key', 'fingerprint')
    can_delete = True
    show_change_link = False

    
class CustomUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + (SshPublicKeyInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


