from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from product.views_dir import auth_view 

urlpatterns = [
    
    ############ admin url ###################
    path('staff-account/', admin.site.urls),

    ############ home url ####################
    path('', views.home, name='home'),


    ############ login & register urls ###################
    path('register/', auth_view.register, name='register'),
    path('login/', auth_view.loginPage, name='login'),
    path('logout/', auth_view.logoutPage, name='logout'),
    

    ############ app urls ###################
    path('', include('product.urls')),
    path('', include('order.urls')),
    path('', include('user.urls')),
    path('', include('payment.urls')),

    ############ error url ###################
    path('error/', views.error, name='error'),


    ############ about url ###################
    path('about/', views.aboutPage, name='about_page'),


    ############ contact urls ###################
    path('contact/', views.contactPage, name='contact_page'),

    ############# privacy policy ###################
    path('privacy-policy/',views.privacyPolicyPage, name='privacy_policy'),
    
    ############# Terms and Conditions ##############################
    path('terms-and-conditions/', views.termsAndConditionsPage, name='terms_and_conditions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
