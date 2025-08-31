from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import requests

def index (request):
    # objeto_atualizado = {
    #     "name": "Apple MacBook Pro 16 2025",
    # }
    #response = requests.get("https://api.restful-api.dev/objects/ff8081819782e69e0198d2b197860b24")
    response = requests.get("https://api.restful-api.dev/objects/ff8081819782e69e0198d2b197860b24")
    print(response.status_code)
    print("---------")
    posts = response.json()
    return JsonResponse(posts, safe=False)