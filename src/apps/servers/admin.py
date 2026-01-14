from django.contrib import admin
from .models import Server, ServerIp, ServerUser, ServerProvider

class ServerIpInline(admin.TabularInline):
    model = ServerIp
    extra = 1
    fields = ('label', 'ip_address', 'ssh_port', 'is_public')

class ServerUserInline(admin.TabularInline):
    model = ServerUser
    extra = 1
    fields = ('username', 'allow_ssh',)

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'organization')
    search_fields = ('name', 'hostname')
    list_filter = ('organization',)

    inlines = [ServerIpInline, ServerUserInline]
    
@admin.register(ServerProvider)
class ServerProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)