from django.shortcuts import render
from django.views.generic import TemplateView

from doorkeeper.decorators import doorkeeper_exempt

# Create your views here.


class HomeView(TemplateView):
    template_name = "demo_app/home.html"


# This view will be accessible without the doorkeeper password
@doorkeeper_exempt
class PublicView(TemplateView):
    template_name = "demo_app/public.html"
