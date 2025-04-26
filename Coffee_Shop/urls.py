from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Base_App import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.HomeView, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.HomeView, name="Home"), 
    path('delivery/', views.DeliveryView, name='order_delivery'),
    path('menu/', views.Menu, name='Menu'),
    path('about/', views.AboutView, name='About'),
    path('cart/', views.CartView, name='Cart'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('delivery_success/', views.DeliverySuccessView, name='delivery_success'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),    
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_order, name='process_order'),
    path('process-order/', views.process_order, name='process_order'),
    path('order-confirmation/<int:delivery_id>/', views.order_confirmation, name='order_confirmation'),
    path('download-receipt/<int:delivery_id>/', views.generate_receipt, name='download_receipt'),
    path('order/<int:order_id>/receipt/', views.generate_receipt, name='generate_receipt'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
