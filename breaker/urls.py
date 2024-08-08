from django.urls import path
from . import views

urlpatterns = [
    path('ping', views.ping, name='ping-gate-1'),
    path('restart/<email>', views.restart),
    path('<email>', views.start),
    path('<email>/<ans>', views.attempt),
]
