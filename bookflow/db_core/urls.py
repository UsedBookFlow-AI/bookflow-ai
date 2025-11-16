from django.urls import path
from db_core.views import RegisterUserView, LoginUserView, StoreInventoryBookView, StoreBookSupplyRequestView, ApplyBookSupplyView, MyPageView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('store_book/', StoreInventoryBookView.as_view(), name='store_inventory_book'),
    path('request_supply/', StoreBookSupplyRequestView.as_view(), name='store_supply_request'),
    path('apply-book-supply/', ApplyBookSupplyView.as_view(), name='apply_book_request'),
    path('mypage/<str:user_id>/', MyPageView.as_view(), name='mypage')
]