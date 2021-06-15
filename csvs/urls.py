from django.urls import path
from .views import add_teacher


app_name = 'csvs'

urlpatterns = [
    path('', add_teacher, name='add-teachers-view'),
]