from django.urls import path
from . import views

urlpatterns = [
    path('signup-company/', views.signup_company, name='signup_company'),
    path('companies/', views.list_companies, name='list_companies'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    path('company/<int:pk>/add-doc/', views.add_doc, name='add_doc'),
    path('document/<int:pk>/del-doc/', views.del_doc, name='del_doc'),
    path('metrics/<int:pk>/add/', views.add_metric, name="add_metric"),
    path('manage-proposal/<int:pk>/', views.manage_proposal, name="manage_proposal"),
]
