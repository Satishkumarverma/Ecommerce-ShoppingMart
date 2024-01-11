from django.urls import path
from app_version1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app_version1.forms import loginForm,UserPasswordChangeForm,UserPasswordResetForm,UserSetPasswordForm

urlpatterns = [
    path('', views.home),
    path('product-detail/<int:p_id>', views.product_detail, name='product-detail'),

    path('search/', views.search, name='search'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('show_to_cart/', views.show_to_cart, name='show-to-cart'),
    path('pluscart/', views.pluscart),
    path('minuscart/', views.minuscart),
    path('removecart/', views.removecart),

    path('paymentdone/', views.paymentdone, name='paymentdone'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=loginForm), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("changepassword/", auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=UserPasswordChangeForm, success_url='/changepassword_done/'), name='changepassword'),
    path("changepassword_done/", auth_views.PasswordChangeDoneView.as_view(template_name='app/changepassword_done.html'), name='changepassword_done'),

    path("passwordreset/", auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html', form_class=UserPasswordResetForm), name='passwordreset'),
    path("passwordreset_done/", auth_views.PasswordResetDoneView.as_view(template_name='app/passwordreset_done.html'), name='password_reset_done'),
    path("passwordreset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordreset_confirm.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path("passwordreset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordreset_complete.html'), name='password_reset_complete'),

    path('customerregistration/', views.customerregistration, name='customerregistration'),


    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
