from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def landingpage(request):
    return redirect('bipage')

def bipage(request):
    return HttpResponse('<iframe title="talos" width="1890" height="980" src="https://app.powerbi.com/reportEmbed?reportId=42648c22-0167-4ccd-a700-4288e0b6462e&autoAuth=true&ctid=900d267a-9bf0-4efa-a7eb-fd79d92c18a8&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWJyYXppbC1zb3V0aC1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>')

def manualApi(request):
    return HttpResponse('pagina reservada para o manual de uso da api') 