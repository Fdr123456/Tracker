from django.contrib import admin
from .models import Company, Vacancy, Application

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'posted_at')
    list_filter = ('status', 'company')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'vacancy', 'status', 'applied_at')
    list_filter = ('status',)

