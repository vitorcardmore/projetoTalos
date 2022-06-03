from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def landingpage(request):
    return redirect('bipage')

def bipage(request):
    return render(request, 'web/dashboard.html')

def manualApi(request):
    return render(request, 'web/manualapi.html')   