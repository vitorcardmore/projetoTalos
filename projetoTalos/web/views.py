from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def landingpage(request):
    return redirect('bipage')

def bipage(request):
    return HttpResponse('pagina de plot com powerbi')

def manualApi(request):
    return HttpResponse('pagina reservada para o manual de uso da api') 