from django.views.generic import TemplateView
from django.http import HttpResponse

# /default
class Default(TemplateView):
    def get(self,request):
        return HttpResponse(status=204)
