from re import template
from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('wishlist/', views.showWishlist, name='wishlist'),
    path('profile/', views.profile, name='profile' ),
    path('profile/add-address/', views.addAddress, name='addAddress'),
    path('profile/update-address/<int:id>', views.updateAddress, name='updateAddress'),
    path('profile/update-profile/', views.profileUpdate, name='profileUpdate'),

    ####################### password reset #######################################
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset_password/sent/', auth_views.PasswordResetDoneView.as_view(template_name='user/reset-password/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/reset-password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password/done/',auth_views.PasswordResetCompleteView.as_view(template_name='user/reset-password/password_reset_complete.html'),name='password_reset_complete'),
]