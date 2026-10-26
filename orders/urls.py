from django.urls import path
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', OrderUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete'),
    path('view/<int:pk>/', OrderDetailView.as_view(), name='view'),
]