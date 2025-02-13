import os

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models

import numpy as np

from PIL import Image


def predict_image(img):
# Cargar el modelo preentrenado
    model = models.resnet34()
    model.load_state_dict(torch.load('resnet34-b627a593-pth'))
    model.eval()  # Cambiar a modo evaluación

    # Transformaciones de la imagen
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalizar según ImageNet
    ])

    # Cargar y transformar la imagen
    #image_path = "/content/car.jpg"  # Ruta de la imagen
    image = Image.open(img).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Agregar batch dimension

    # Realizar inferencia sin calcular gradientes
    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)  # Aplicar softmax para obtener probabilidades
        predicted_class = torch.argmax(probabilities).item()  # Obtener el índice de la clase con mayor probabilidad

    # Cargar etiquetas de ImageNet
    labels_map = models.ResNet101_Weights.IMAGENET1K_V1.meta["categories"]
    predicted_label = labels_map[predicted_class]  # Obtener el nombre de la categoría

    print(f"Predicción: {predicted_label} (Clase {predicted_class})")
    
    return predicted_label


if __name__ == '__main__':
    predict_image('cat.jpg')