from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login_view),
    path('seller/',
         seller_dashboard),

    path('add-product/',
         add_product),

    path('products/',
         view_products),

    path('update-product/<int:id>/',
         update_product),

    path('delete-product/<int:id>/',
         delete_product),
    path(
        'customer-dashboard/',
        customer_dashboard
    ),

    path(
        'all-products/',
        view_all_products
    ),

    # Wishlist
    path(
        'add-to-wishlist/<int:id>/',
        add_to_wishlist
    ),

    path(
        'view-wishlist/',
        view_wishlist
    ),

    path(
        'remove-wishlist/<int:id>/',
        remove_wishlist
    ),

    # Cart
    path(
        'add-to-cart/<int:id>/',
        add_to_cart
    ),

    path(
        'view-cart/',
        view_cart
    ),

    path(
        'remove-cart/<int:id>/',
        remove_cart
    ),

    # Orders
    path(
        'place-order/',
        place_order
    ),

    path(
        'view-orders/',
        view_orders
    ),

    path(
        'cancel-order/<int:id>/',
        cancel_order
    ),

    # Reviews
    path(
        'add-review/<int:id>/',
        add_review),
    path(
        'product-reviews/<int:id>/',
        view_product_reviews
    ),
    # Profile & Address Routing
    path(
        'profile/edit/',
        edit_profile
    ),
    path(
        'address/add/',
        add_address
    ),
    path(
        'address/delete/<int:id>/',
        delete_address
    ),
    # Product Details Page
    path(
        'product/<int:id>/',
        product_detail
    ),
    path(
        'logout/',
        logout
    )
]
