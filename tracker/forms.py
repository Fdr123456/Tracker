from django import forms
from .models import Company, Vacancy

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'city', 'website', 'description']

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['company', 'title', 'salary_min', 'salary_max', 'status']