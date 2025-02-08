# from django.urls import path
# from .views import dashboard_view

# urlpatterns = [
#     path('', dashboard_view, name='dashboard'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update_charts/', views.update_charts, name='update_charts'),
]
