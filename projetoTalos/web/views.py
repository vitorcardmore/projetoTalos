from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def landingpage(request):
    return redirect('bipage')

def bipage(request):
    return HttpResponse('<iframe title="talos - Página 1" width="100%" height="100%" src="https://app.powerbi.com/view?r=eyJrIjoiMGM1YmM4ZGYtMGE2My00NWY0LWI4OTQtYmIxNjE2NTcwZGI5IiwidCI6ImUxOWVhYzBhLTJiZWEtNGYxMi04Yzg3LWNkNzk5YTg0MDhhZCJ9" frameborder="0" allowFullScreen="false"></iframe>')

def manualApi(request):
    return HttpResponse('pagina reservada para o manual de uso da api')     