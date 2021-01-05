from django.urls import path

from . import views

app_name = "customer"

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create', views.create_view, name='create'),
    path('processing', views.processing_view, name='processing'),
    path('completed', views.completed_view, name='completed'),
    path('manage/processing', views.manage_processing_view, name='manage_processing'),
    path('manage/completed', views.manage_completed_view, name='manage_completed'),
    path('manage/due', views.manage_due_view, name='manage_due'),
    path("edit/<int:request_id>", views.edit_view, name="edit"),
    path("search", views.search_view, name='search'),
    path("download", views.csv_view, name='download')
]