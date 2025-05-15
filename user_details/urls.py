from django.urls import path
from .views import AllUsersListView , TotalUsersView , TotalBooksView , UserInfoView,UserProfileView

urlpatterns = [
    path('users/', AllUsersListView.as_view(), name='all-users'),
    path('total-user/', TotalUsersView.as_view(), name='total-users'),
    path('total-books/', TotalBooksView.as_view(), name='total-books'),
    path('users/<int:id>/', UserInfoView.as_view(), name='user-detail'),
    path('user-profile/', UserProfileView.as_view(), name='full_user_profile'),
]