from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('logout/', views.logout, name='logout'),
]
