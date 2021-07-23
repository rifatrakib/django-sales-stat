from django.urls import path

from .views import (
    SalesListView, SalesDetailView,
    home_view,
)


app_name = 'sales'
urlpatterns = [
    path('', home_view, name='home'),
    path('list/', SalesListView.as_view(), name='list'),
    path('sales/<pk>/', SalesDetailView.as_view(), name='detail'),
]
