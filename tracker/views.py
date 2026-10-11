from django.views.generic import ListView, DetailView, CreateView
from .models import Company, Vacancy
from django.urls import reverse_lazy
from .forms import CompanyForm, VacancyForm

class CompanyListView(ListView):
    model = Company
    template_name = 'tracker/company_list.html'
    context_object_name = 'companies'
    ordering = ['id']

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'tracker/company_detail.html'
    context_object_name = 'company'

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'tracker/company_form.html'
    success_url = reverse_lazy('company_list')

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'tracker/vacancy_list.html'
    context_object_name = 'vacancies'
    ordering = ['id']

class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'tracker/vacancy_detail.html'
    context_object_name = 'vacancy'

class VacancyCreateView(CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'tracker/vacancy_form.html'
    success_url = reverse_lazy('vacancy_list')