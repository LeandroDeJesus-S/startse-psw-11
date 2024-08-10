from django.urls import path
from . import views

urlpatterns = [
    path('suggestions/', views.suggestions, name='suggestions'),
    path('company/<int:pk>', views.see_company, name='see_company'),
    path('company/<int:pk>/propose/', views.propose, name='propose'),
    path('contract/<int:pk>/', views.contract, name='contract'),
]
