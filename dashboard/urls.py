from django.urls import path
from dashboard.views import *

urlpatterns = [

    # USER HOME (home page)
    path('home', home, name="home"),

    # ADMIN DASHBOARD
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    path('orders/', manage_orders, name="manage_orders"),
    path('update/<int:order_id>/', update_status, name="update_status"),
]

