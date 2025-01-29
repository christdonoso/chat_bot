from django.shortcuts import render
from django.http import JsonResponse
from .agent import run_agent
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def chat(request):
    return render(request,'index.html')

@csrf_exempt
def get_response(request):
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    message = run_agent(json_data['message'])
    print(message)
    return JsonResponse({'message':message})