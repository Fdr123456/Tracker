from rest_framework import serializers
from .models import Company, Vacancy, Application

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'company', 'company_name', 'salary_min', 'salary_max', 'status', 'posted_at']


class ApplicationSerializer(serializers.ModelSerializer):
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'user_email', 'vacancy', 'vacancy_title', 'applied_at', 'status', 'notes']
