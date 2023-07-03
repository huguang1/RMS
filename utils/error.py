from django.views.generic import View
from django.shortcuts import render

class Error404(View):
    def get(self, request):
        return render(request, 'error404.html')