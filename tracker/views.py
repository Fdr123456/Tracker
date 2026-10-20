import logging
import json
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Company, Vacancy, Application
from .forms import CompanyForm, VacancyForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


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


def kanban_data(request):
    try:
        apps = Application.objects.filter(
            vacancy__isnull=False
        ).select_related('vacancy', 'vacancy__company').order_by('status', 'position')

        board = {
            'applied': [],
            'call': [],
            'task': [],
            'final': [],
            'accepted': [],
            'rejected': [],
        }

        for app in apps:
            vacancy_title = (
                app.vacancy.title
                if (app.vacancy and app.vacancy.title)
                else 'Без вакансии'
            )

            company_name = (
                app.vacancy.company.name
                if (app.vacancy and app.vacancy.company and app.vacancy.company.name)
                else 'Без компании'
            )

            status_key = app.status if app.status in board else 'applied'

            board[status_key].append({
                'id': app.id,
                'vacancy_title': vacancy_title,
                'company_name': company_name,
                'status': status_key,
                'applied_at': app.applied_at.isoformat() if app.applied_at else None,
                'notes': app.notes or '',
                'position': app.position,
            })

        return JsonResponse(board, safe=False)

    except Exception as e:
        logger.error("Ошибка в kanban_data: %s", e, exc_info=True)
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)


@require_http_methods(["PATCH", "DELETE"])
def update_application_status(request, pk):
    try:
        app = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'DELETE':
        app.delete()
        return JsonResponse({"status": "success", "message": "Отклик удалён"})

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if 'status' in data:
        if data['status'] in ['applied', 'call', 'task', 'final', 'accepted', 'rejected']:
            app.status = data['status']

    if 'notes' in data:
        raw = data['notes']
        app.notes = raw.strip() if (raw and raw.strip()) else None

    if 'position' in data:
        pos = data['position']
        if isinstance(pos, int) and pos >= 0:
            app.position = pos

    app.save()
    return JsonResponse({
        'status': 'success',
        'new_status': app.status,
        'notes': app.notes,
        'id': app.id
    })


@require_http_methods(["POST"])
def create_application(request):
    try:
        data = json.loads(request.body)
        vacancy_id = data.get("vacancy_id")

        if not vacancy_id:
            return JsonResponse({"error": "vacancy_id обязателен"}, status=400)

        vacancy = Vacancy.objects.select_related("company").get(pk=vacancy_id)

        app = Application.objects.create(
            vacancy=vacancy,
            status="applied",
            notes=None,
        )

        return JsonResponse({
            "id": app.id,
            "vacancy_title": vacancy.title,
            "company_name": vacancy.company.name if vacancy.company else "Без компании",
            "status": app.status,
            "notes": app.notes or "",
        }, status=201)

    except Vacancy.DoesNotExist:
        return JsonResponse({"error": "Вакансия не найдена"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error("Ошибка в create_application: %s", e, exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["DELETE"])
def delete_application(request, pk):
    try:
        application = Application.objects.get(id=pk)
        application.delete()
        return JsonResponse({"status": "success", "message": "Отклик удален"})
    except Application.DoesNotExist:
        return JsonResponse({"error": "Отклик не найден"}, status=404)
    except Exception as e:
        logger.error("Ошибка в delete_application: %s", e, exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def debug_save(request, pk):
    try:
        if not request.body:
            return JsonResponse({'success': False, 'error': 'Empty request body'}, status=400)

        data = json.loads(request.body)
        app = Application.objects.get(pk=pk)

        # Заметки
        if 'notes' in data:
            raw_notes = data['notes']
            if raw_notes is None:
                app.notes = None
            else:
                stripped = str(raw_notes).strip()
                app.notes = stripped if stripped else None

        # Статус
        if 'status' in data:
            status_value = data['status']
            valid_statuses = ['applied', 'call', 'task', 'final', 'accepted', 'rejected']
            if status_value in valid_statuses:
                app.status = status_value

        # Позиция
        if 'position' in data:
            pos = data['position']
            if isinstance(pos, int) and pos >= 0:
                app.position = pos

        app.save()

        return JsonResponse({
            'success': True,
            'id': app.id,
            'status': app.status,
            'position': app.position,
            'notes': app.notes
        })

    except Application.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error("Ошибка в debug_save: %s", e, exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
