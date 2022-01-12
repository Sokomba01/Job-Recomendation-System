from django.contrib import admin
from .models import *
from .resources import Job_Dataset
from import_export.admin import ImportExportModelAdmin
admin.site.register(Signup)
admin.site.register(UserResumes)
# admin.site.register(Job_Dataset)
admin.site.register(JobPublish)
admin.site.register(template)
@admin.register(Job_Dataset)
class PostAdmin(admin.ModelAdmin):
    list_display = ['JobTitle','Company','Location','PostDate', 'Summary','Salary','JobUrl']
class ViewAdmin(ImportExportModelAdmin):
    pass
# #     resource_class = PropertyAdminResource