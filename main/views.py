import os
import json

from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from django.conf import settings

from torchvision import models

from .agent import run_agent
from .resnet import predict_image
# Create your views here.


def chat(request):
    return render(request,'index.html')

@csrf_exempt
def get_response(request):
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    message = run_agent(json_data['message'])
    print(message)
    # Message.objects.create(
    #     user_message = json_data['message'],
    #     bot_message = message
    # )
    return JsonResponse({'message':message})


def bd(request):
    db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")

    # Retornar el archivo como una respuesta de descarga
    return FileResponse(
        open(db_path, "rb"), 
        as_attachment=True, 
        filename="db.sqlite3"
    )


def pose_recognition(request):
    return render(request, 'pose_recognition.html')


@csrf_exempt
def upload_img(request):
    if request.method == 'GET':
        return render(request, 'upload_img.html')
    else:
        image = request.FILES.get('image')
        print(image)
        result = predict_image(image)
        return JsonResponse({'result': result})
