from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.servers.models import Server
from .models import (
    Project,
    EnvironmentMode, Environment, 
    OdooEnvironment, OdooDatabase, OdooConfiguration, OdooPath,
    DockerEnvironment, DockerService
)

admin.site.register(EnvironmentMode)
admin.site.register(Project)

class OdooDatabaseInline(admin.TabularInline):
    model = OdooDatabase
    extra = 1
    fields = ('name',)

class OdooConfigurationInline(admin.TabularInline):
    model = OdooConfiguration
    extra = 1
    fields = ('key', 'value')

class OdooPathInline(admin.TabularInline):
    model = OdooPath
    extra = 1
    fields = ('path_type', 'path', 'own_addons', 'oca_addons', 'store_addons', 'other_addons')

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(OdooEnvironment)
class OdooEnvironmentAdmin(admin.ModelAdmin):
    inlines = [OdooDatabaseInline, OdooConfigurationInline, OdooPathInline]

@admin.register(DockerService)
class DockerServiceAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(DockerEnvironment)
class DockerEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('environment', 'compose_file_path', 'services_link')
    search_fields = ('environment__name',)

    def services_link(self, obj):
        url = (
            reverse("admin:environments_dockerservice_changelist")
            + f"?environment__id__exact={obj.id}"
        )

        link_text = f"{obj.services.count()} servicio(s)"
        return format_html(f'<a href="{url}">{link_text}</a>')

    services_link.short_description = "Servicios" 