from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  # ✅ Use signup, not register
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clothing/', views.clothing_list, name='clothing_list'),
    path('try-on/<int:clothing_id>/', views.try_on, name='try_on'),
]
