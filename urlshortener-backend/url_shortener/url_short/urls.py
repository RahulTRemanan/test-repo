from django.urls import path
from .import views

urlpatterns = [
    path('api/shorten',views.shorten),
    path('api/info/<str:code>',views.link_info),
    path('<str:code>',views.redirect_link)
]