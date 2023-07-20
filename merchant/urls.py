from django.urls import path
from .views import MerchantRegisterView, LoginView, MerchantChangePasswordView, MerchantPasswordChangeEmailSendView, MerchantResetPasswordView

urlpatterns = [
    path('merchantregister', MerchantRegisterView.as_view(),name='merchant-register'),
    path('merchantlogin', LoginView.as_view(),name='merchant-login'),
    path('changepassword', MerchantChangePasswordView.as_view(),name='merchant-change-password'),
    path('send', MerchantPasswordChangeEmailSendView.as_view(),name='merchant-change-password-send'),
    path('reset/<uid>/<token>', MerchantResetPasswordView.as_view(),name='merchant-change-password-reset'),
]