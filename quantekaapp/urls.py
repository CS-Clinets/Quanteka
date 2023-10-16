from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.index),
    path('about/', v.about),
    path('contact/', v.contact),
    path('services/', v.services),
    path('onepage/', v.onepage),

    # login
    path('accounts/login/',v.accountlogin, name="accountlogin"),
    path('login/', v.loginPage, name="login"),



    # logout
    path('logout/',v.mylogout),

    # register
    path('register/', v.register),
    path('verify-otp/', v.register_final),


    path('otp2/', v.otp2),

    # footer
    path('footer/', v.footer),
    
    
    # dashboard Page
    path('dashboard/', v.dashboard),

    # Report Detail
    path('report-detail/',v.report_detail, name='report_detail'),
    
    # Overview
    path('overview/', v.overview),

    path('getembedinfo/', v.get_embed_info, name="getembedinfo"),

]
