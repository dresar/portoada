from django.shortcuts import render

def handler400(request, exception=None):
    """
    Handler for 400 Bad Request errors
    """
    return render(request, '400.html', status=400)

def handler403(request, exception=None):
    """
    Handler for 403 Forbidden errors
    """
    return render(request, '403.html', status=403)

def handler404(request, exception=None):
    """
    Handler for 404 Page Not Found errors
    """
    return render(request, '404.html', status=404)

def handler500(request):
    """
    Handler for 500 Internal Server Error
    """
    return render(request, '500.html', status=500)