from django.shortcuts import render
from django.views.generic.list import ListView

from account.models import Account

class HomeView(ListView):
    model = Account
    template_name = 'public/index.html'
