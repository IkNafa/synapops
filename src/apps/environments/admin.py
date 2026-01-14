from django.contrib import admin
from django import forms

from apps.servers.models import Server
from .models import EnvironmentMode, Environment, OdooEnvironment, OdooDatabase, OdooConfiguration, OdooPath

admin.site.register(EnvironmentMode)

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