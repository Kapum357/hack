from django.contrib.gis import admin
from .models import FloodThreat, SocialVulnerability


@admin.register(FloodThreat)
class FloodThreatAdmin(admin.GISModelAdmin):
    list_display = ('name', 'threat_level', 'created_at')
    list_filter = ('threat_level', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SocialVulnerability)
class SocialVulnerabilityAdmin(admin.GISModelAdmin):
    list_display = ('name', 'vulnerability_index', 'affected_population', 'linked_families', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
