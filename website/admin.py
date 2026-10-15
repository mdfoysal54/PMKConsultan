from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import SiteSettings, Section, Service, Industry, Inquiry, Portfolio, AuditEvent

admin.site.site_header='PMK • Control Center'
admin.site.site_title='PMK Administration'
admin.site.index_title='Content, leads and operations'

class AuditedAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        super().save_model(request,obj,form,change)
        AuditEvent.objects.create(actor=str(request.user.pk),action='update' if change else 'create',model=obj._meta.label,object_id=str(obj.pk),summary=str(obj)[:250])
    def delete_model(self,request,obj):
        AuditEvent.objects.create(actor=str(request.user.pk),action='delete',model=obj._meta.label,object_id=str(obj.pk),summary=str(obj)[:250])
        super().delete_model(request,obj)
    def delete_queryset(self,request,queryset):
        for obj in queryset:
            AuditEvent.objects.create(actor=str(request.user.pk),action='delete',model=obj._meta.label,object_id=str(obj.pk),summary=str(obj)[:250])
        super().delete_queryset(request,queryset)

@admin.register(SiteSettings)
class SiteSettingsAdmin(AuditedAdmin):
    list_display=('company_name','tagline','updated_at')
    def has_add_permission(self,request): return super().has_add_permission(request) and not SiteSettings.objects.exists()
    def has_delete_permission(self,request,obj=None): return False

@admin.register(Section)
class SectionAdmin(AuditedAdmin):
    list_display=('key','heading','enabled','updated_at')
    list_filter=('enabled',)
    search_fields=('key','heading')

@admin.register(Service)
class ServiceAdmin(AuditedAdmin):
    list_display=('title','order','published')
    list_editable=('order','published')
    prepopulated_fields={'slug':('title',)}

@admin.register(Industry)
class IndustryAdmin(AuditedAdmin):
    list_display=('name','order','published')
    list_editable=('order','published')
    prepopulated_fields={'slug':('name',)}

@admin.register(Portfolio)
class PortfolioAdmin(AuditedAdmin):
    list_display=('title','category','is_demo','is_published','featured')
    list_filter=('is_demo','is_published','featured')
    prepopulated_fields={'slug':('title',)}

@admin.register(Inquiry)
class InquiryAdmin(AuditedAdmin):
    list_display=('name','email','company','service','status','created_at')
    list_filter=('status','service','created_at')
    search_fields=('name','email','company')
    readonly_fields=('name','email','company','service','budget','details','created_at')
    def has_add_permission(self,request): return False

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display=('timestamp','actor','action','model','object_id','summary')
    list_filter=('action','model')
    search_fields=('actor','model','summary')
    def has_add_permission(self,request): return False
    def has_change_permission(self,request,obj=None): return False
    def has_delete_permission(self,request,obj=None): return False
