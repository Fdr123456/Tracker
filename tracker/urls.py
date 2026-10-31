from django.urls import path
from django.views.generic.base import RedirectView
from .views import CompanyListView, VacancyListView, VacancyDetailView, VacancyCreateView, kanban_data
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/companies/', permanent=False)),

    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('company/new/', views.CompanyCreateView.as_view(), name='company_create'),
    path('api/companies/', views.api_companies_list, name='api_companies'),

    path('vacancies/', VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy/<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancy/new/', VacancyCreateView.as_view(), name='vacancy_create'),

    path('api/kanban/', views.kanban_data, name='kanban_data'),
    path('api/applications/', views.create_application, name='create_application'),

    path('api/application/<int:pk>/', views.update_application_status, name='app_update'),
    path('api/application/<int:pk>/delete/', views.delete_application, name='delete_application'),

    path('application/create/', views.create_application, name='create_application'),

    path('api/debug/<int:pk>/', views.debug_save, name='debug_save'),

    path('api/vacancies/', views.api_vacancies_list, name='api_vacancies'),
]

