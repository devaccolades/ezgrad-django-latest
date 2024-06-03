from django.contrib import admin
from service.models import ServiceType,CourseType

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'service',
    ]
admin.site.register(ServiceType,ServiceTypeAdmin)

class CourseTypeAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'service',
        'course_type',
    ]
admin.site.register(CourseType,CourseTypeAdmin)

# Register your models here.
