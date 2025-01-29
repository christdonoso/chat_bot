from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from .agent import run_agent
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import os
from django.conf import settings
# Create your views here.


def chat(request):
    return render(request,'index.html')

@csrf_exempt
def get_response(request):
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    message = run_agent(json_data['message'])
    print(message)
    Message.objects.create(
        user_message = json_data['message'],
        bot_message = message
    )
    return JsonResponse({'message':message})


def bd(request):
    db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")

    # Retornar el archivo como una respuesta de descarga
    return FileResponse(
        open(db_path, "rb"), 
        as_attachment=True, 
        filename="db.sqlite3"
    )