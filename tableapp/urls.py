from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("menu/", views.dashboard_signup, name="menu"),
    path("menu/<int:pk>/edit", views.edit_menu, name="menu_edit"),
    path("menu/<int:pk>/delete/", views.delete_menu, name="menu_delete"),
    path("menu/<slug:menu_url>/<int:pk>/category", views.dashboard_category, name="menu_category"),
    path("menu/category/edit", views.edit_category, name="category_edit"), # id is passed in the form as a hidden input
    path("menu/category/delete", views.delete_category, name="category_delete"), #id is passed in the form as a hidden input
    path("menu/category/<slug:category_url>/<int:pk>/items", views.dashboard_item, name="menu_items"),
    path("menu/item/delete", views.delete_item, name="item_delete"),
    path("menu/item/edit", views.edit_item, name="item_edit"),
    path("menu/<slug:pk>/display", views.display_items, name="all_items"),
    path("menu/<slug:category>/<slug:item>/add", views.add_existing, name="existing_item"),
    path("menu/<slug:menu_url>/<int:pk>/qrcode", views.get_qr, name="qrcode"),
    path("menu/<slug:menu_url>/<int:pk>/category/<int:table_number>", views.user_dashboard_category, name="table_menu_category"),
    path("menu/<slug:menu_url>/<int:category_id>/item/<int:table_number>", views.user_dashboard_item, name="table_menu_item"),
    path("menu/cart/add/<int:menu_id>/<int:category_id>", views.add_cart_item, name="cart_items"),
    path("menu/cart/viewcart/<int:menu_id>/<int:table_id>", views.view_cart, name="view_cart"),
    path("menu/cart/editcart/<int:cart_id>/<int:item_id>/<slug:option>", views.edit_cart, name="delete_cart"),
    path("menu/checkout/<int:cart_id>", views.checkout, name="checkout"),
    path("menu/submit/<int:cart_id>", views.submit, name="submit"),
    path("vieworder/", views.view_order, name="view_order"),
    path("completeOrder/<int:order_id>", views.complete_order, name="complete_order"),
    path("menu/subscriptions", views.subscription, name="get_subscriptions")
]