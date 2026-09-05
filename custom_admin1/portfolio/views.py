from django.shortcuts import redirect

def home(request):
    """
    Redirect root URL to portfolio admin login page
    """
    return redirect('/portfolio-admin/login/')