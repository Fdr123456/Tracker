from django.views.generic import ListView, DetailView, CreateView
from .models import Company, Vacancy, Application
from django.urls import reverse_lazy
from .forms import CompanyForm, VacancyForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

@login_required
def kanban_data(request):
    apps = Application.objects.filter(user=request.user).select_related('vacancy', 'vacancy_company')
    board ={
        'applied': [],
        'call': [],
        'task': [],
        'final': [],
        'accepted': [],
        'rejected': [],
    }
    for app in apps:
        board[app.status].append({
            'id': app.id,
            'vacancy_title': app.vacancy.title,
            'company_name': app.vacancy.company.name,
            'status': app.status,
            'applied_at': app.applied_at.isoformat(),
            'notes': app.notes,
        })
    return JsonResponse(board)