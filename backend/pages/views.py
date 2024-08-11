from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return render(request, 'index.html')

# pero based sa nababasa ko, baka di na to kailangan since for vue
# common ang single page na maghandle sa lahat o mostly
def about(request):
  return render(request, 'pages/about.html')