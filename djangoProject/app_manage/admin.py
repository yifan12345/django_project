from django.contrib import admin
from app_manage.models import Project


# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'describe', 'create_time', 'update_time']
    search_fields = ['name']  # 搜索栏
    list_filter = ['status']  # 过滤器


admin.site.register(Project, ProjectAdmin)
