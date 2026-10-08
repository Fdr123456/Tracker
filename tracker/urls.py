from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import CompanyListView, VacancyListView, VacancyDetailView, VacancyCreateView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/companies/', permanent=False)),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('vacancies/', VacancyListView.as_view(), name='vacancy_list'),
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('company/new/', views.CompanyCreateView.as_view(), name='company_create'),
    path('vacancies/', VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy/<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancy/new/', VacancyCreateView.as_view(), name='vacancy_create'),
]

