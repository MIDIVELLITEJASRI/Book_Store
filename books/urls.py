from django.urls import path # type: ignore
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginUser, name="login"),
    path('signup/', views.signup, name="signup"),
    path('book/<int:book_id>/', views.product_details, name='product_details'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy/<int:book_id>/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('logout/', views.logoutUser, name='logout'),
    path('login-required/', views.login_required_prompt, name='login_required_prompt'),


]
