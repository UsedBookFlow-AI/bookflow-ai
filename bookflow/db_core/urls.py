from django.urls import path
from db_core.views import RegisterUserView, LoginUserView, StoreInventoryBookView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('store_book/', StoreInventoryBookView.as_view(), name='store_inventory_book'),
]