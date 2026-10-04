from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render
import datetime
import os


def health_check_view(request):
    """
    Automated health check probe for Jenkins, Docker, and Ansible/Puppet.
    Verifies application liveness and database connectivity.
    """
    db_status = 'ok'
    status_code = 200
    try:
        connection.ensure_connection()
    except Exception as exc:
        db_status = f'error: {str(exc)}'
        status_code = 503

    payload = {
        'status': 'healthy' if status_code == 200 else 'unhealthy',
        'application': 'Supplier Quality Review Portal',
        'student': 'AADITYA ASWALE (23102B0044)',
        'database': db_status,
        'environment': os.environ.get('ENVIRONMENT', 'local-development'),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'version': '1.0.0'
    }

    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        return JsonResponse(payload, status=status_code)

    return JsonResponse(payload, status=status_code)


def custom_403_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def custom_404_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)
