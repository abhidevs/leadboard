from django.urls import path

from .views import lead_create, lead_delete, lead_list, lead_detail, lead_update

app_name = "leads"

urlpatterns = [
    path('', lead_list, name='lead-list'),
    path('<int:pk>/', lead_detail, name='lead-detail'),
    path('create/', lead_create, name='lead-create'),
    path('<int:pk>/update/', lead_update, name='lead-update'),
    path('<int:pk>/delete/', lead_delete, name='lead-delete'),
]
