from django.shortcuts import render

    
def home(request):
    """
    Controller for the app home page.
    """
    context = {'nav': 'home'}
    return render(request, 'parleys_creek_management/home.html', context)