from django.urls import path
from .views import index, SignInView, AccountLogoutView, AccountDetailView, \
    AccountUpdateView, DeleteProfileView

app_name = 'profiles'

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('log-out/', AccountLogoutView.as_view(), name='log_out'),
    path('detail-account/<int:pk>/', AccountDetailView.as_view(), name='detail'),
    path('update-account/<int:pk>/', AccountUpdateView.as_view(), name='update'),
    path('delete-profile/<int:pk>/', DeleteProfileView.as_view(), name='delete'),
    path('', index, name='index'),
]