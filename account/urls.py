from django.urls import path
from .views import (
                    register_view, logout_view, login_view, account_view, 
                    edit_account_view, edit_profile_image_view,
                    edit_user_profile_view
                    )
from .forms import (PwdResetConfirmForm, PwdResetForm)


from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


app_name = "account"

urlpatterns = [
     # Reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/user/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm',
                                                                 email_template_name='account/user/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/user/password_reset_confirm.html',
                                                                                                success_url='password_reset_complete',
                                                                                                form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/user/reset_status.html"), name='password_change_done'),
    path('password_reset_confirm/Mg/password_reset_complete/',
         TemplateView.as_view(template_name="account/user/reset_status.html"), 
         name='password_reset_complete'),

    # End of Reset Password



    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<user_id>/', account_view, name='user-account-view'),
    path('<user_id>/edit/', edit_account_view, name='edit-account'),
    path('<user_id>/profile-image/edit/', edit_profile_image_view, name='edit-profile-image'),
    # Profile  
    path('<user_id>/profile/update/', edit_user_profile_view, name='edit-user-profile-view'),
]