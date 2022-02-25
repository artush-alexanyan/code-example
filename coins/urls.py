"""The main application's URLs."""
from django.urls import path

from . import views

app_name = "coins"
urlpatterns = [
    path('', views.coins, name='coins'),
    path('collect-capsule', views.collect_capsule, name='collect_capsule'),
    path('secret-capsule', views.secret_capsule, name='secret_capsule'),
    path('secret-capsule/open', views.secret_capsule_open, name='secret_capsule_open'),
]
