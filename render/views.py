from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'render/index.html', {})

def healthz(request):
    return JsonResponse({'status': 'ok'})
