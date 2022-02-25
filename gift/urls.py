from gift import views
from django.urls import path

urlpatterns = [
    path('apply-code/<str:code>', views.apply_code, name='apply_code'),
]
