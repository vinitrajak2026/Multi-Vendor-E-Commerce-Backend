from django.shortcuts import render
import jwt
from .authentication import (
    is_authenticated,
    seller_required,
    customer_required,
    admin_required
)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .user_serializer import UserSerializer
from .authentication import is_authenticated

SECRET_KEY = 'django-insecure-x)@i5h6la(0z2ri&s(4%33gypfet75g+gep2%o5wbvnab(rt)0'
# Create your views here.
import jwt



def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Usermodel.objects.filter(
            email=email,
            password=password
        )

        if user.exists():

            user = user.first()

            payload = {
                "email": user.email,
                "role": user.role
            }

            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm="HS256"
            )

            request.session['token'] = token
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == "seller":
                return redirect('/flipazon/seller/')

            elif user.role == "customer":
                return redirect('/flipazon/customer-dashboard/')

            elif user.role == "admin":
                return redirect('/flipazon/admin-dashboard/')

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid Credentials'
            }
        )

    return render(
        request,
        'login.html'
    )
@api_view(['POST'])
def register(request):
    try:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Registration Successful",
                "data": serializer.data
            })

        return Response(serializer.errors)

    except Exception as e:
        return Response({
            "error": str(e)
        })


from django.shortcuts import render, redirect
import jwt


@is_authenticated
@seller_required
def seller_dashboard(request):

    seller_id = request.session.get('user_id')

    if not seller_id:
        return redirect('/flipazon/login/')

    seller = Usermodel.objects.get(id=seller_id)
    products = ProductModel.objects.filter(
        seller_id=seller_id
    )
    product_count = products.count()
    orders = OrderModel.objects.filter(product__seller_id=seller_id)
    order_count = orders.count()
    pending_orders = orders.filter(status='pending').count()
    total_sales = sum(o.total_price for o in orders)

    return render(
        request,
        'seller_dashboard.html',
        {
            'seller': seller,
            'products': products,
            'product_count': product_count,
            'order_count': order_count,
            'pending_orders': pending_orders,
            'total_sales': total_sales
        }
    )

@is_authenticated
@seller_required
def add_product(request):

    seller_id = request.session.get('user_id')

    if not seller_id:
        return redirect('/flipazon/login/')

    seller = Usermodel.objects.get(id=seller_id)

    if request.method == "POST":
        pimage_type1 = request.POST.get('pimage_type1', 'link')
        pimage_type2 = request.POST.get('pimage_type2', 'link')
        pimage1_url = request.POST.get('pimage1_url')
        pimage2_url = request.POST.get('pimage2_url')
        pimage1_file = request.FILES.get('pimage1_file')
        pimage2_file = request.FILES.get('pimage2_file')

        ProductModel.objects.create(
            seller=seller,
            pname=request.POST.get('pname'),
            ptype=request.POST.get('ptype'),
            pprice=request.POST.get('pprice'),
            pquantity=request.POST.get('pquantity'),
            pdescription=request.POST.get('pdescription', 'No description available.'),
            pimage_type1=pimage_type1,
            pimage1_url=pimage1_url,
            pimage1_file=pimage1_file,
            pimage_type2=pimage_type2,
            pimage2_url=pimage2_url,
            pimage2_file=pimage2_file
        )

        return render(
            request,
            'success.html',
            {'message': 'Product Added Successfully',
             "dashboard_url": "/flipazon/seller/"}
        )

    return render(request, 'add_product.html')

@is_authenticated
@seller_required
def view_products(request):

    seller_id=request.session['user_id']

    products=ProductModel.objects.filter(
        seller_id=seller_id
    )

    return render(
        request,
        'product_list.html',
        {
            'products':products
        }
    )

@is_authenticated
@seller_required
def delete_product(request,id):

    product = ProductModel.objects.get(
        pid=id
    )

    product.delete()

    return render(
        request,
        'success.html',
        {
            "message":"Product Deleted Successfully",
            "dashboard_url": "/flipazon/seller/"
        }
    )

@is_authenticated
@seller_required
def update_product(request,id):

    product = ProductModel.objects.get(
        pid=id
    )

    if request.method == "POST":

        product.pname = request.POST.get('pname')
        product.ptype = request.POST.get('ptype')
        product.pprice = request.POST.get('pprice')
        product.pquantity = request.POST.get('pquantity')
        product.pdescription = request.POST.get('pdescription', 'No description available.')
        
        product.pimage_type1 = request.POST.get('pimage_type1', 'link')
        product.pimage1_url = request.POST.get('pimage1_url')
        if request.FILES.get('pimage1_file'):
            product.pimage1_file = request.FILES.get('pimage1_file')
            
        product.pimage_type2 = request.POST.get('pimage_type2', 'link')
        product.pimage2_url = request.POST.get('pimage2_url')
        if request.FILES.get('pimage2_file'):
            product.pimage2_file = request.FILES.get('pimage2_file')

        product.save()

        return render(
            request,
            'success.html',
            {
                "message":"Product Updated Successfully",
                "dashboard_url": "/flipazon/seller/"
            }
        )

    return render(
        request,
        'update_product.html',
        {
            "product":product
        }
    )

from django.shortcuts import render,redirect

from django.shortcuts import render, redirect

from django.shortcuts import render, redirect

@is_authenticated
@customer_required
def customer_dashboard(request):

    if request.session.get('role') != 'customer':
        return redirect('/flipazon/login/')

    customer_id = request.session.get('user_id')
    customer = Usermodel.objects.get(id=customer_id)
    cart_count = CartModel.objects.filter(customer=customer).count()
    wishlist_count = WishlistModel.objects.filter(customer=customer).count()
    order_count = OrderModel.objects.filter(customer=customer).count()
    sellers = Usermodel.objects.filter(role="seller").exclude(shop_name__isnull=True).exclude(shop_name="")

    return render(
        request,
        'customer_dashboard.html',
        {
            'customer': customer,
            'cart_count': cart_count,
            'wishlist_count': wishlist_count,
            'order_count': order_count,
            'sellers': sellers
        }
    )
from django.db.models import Avg

@is_authenticated
@customer_required
def view_all_products(request):
    products = ProductModel.objects.all()

    # Get filter and sort parameters
    category = request.GET.get('category')
    stock_only = request.GET.get('stock')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by')

    # Apply filters
    if category:
        products = products.filter(ptype=category)
    if stock_only == 'true':
        products = products.filter(pquantity__gt=0)
    if min_price:
        products = products.filter(pprice__gte=min_price)
    if max_price:
        products = products.filter(pprice__lte=max_price)

    # Sort
    if sort_by == 'price_asc':
        products = products.order_by('pprice')
    elif sort_by == 'price_desc':
        products = products.order_by('-pprice')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # Build products lists with reviews
    product_data = []
    for product in products:
        avg_rating = ReviewModel.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        product_data.append({
            'product': product,
            'avg_rating': round(avg_rating,1) if avg_rating else 0
        })

    # Sort by rating on the list if requested
    if sort_by == 'rating_desc':
        product_data.sort(key=lambda x: x['avg_rating'], reverse=True)

    # Get all distinct categories for filter dropdown
    categories = ProductModel.objects.values_list('ptype', flat=True).distinct()

    return render(
        request,
        'all_products.html',
        {
            'products': product_data,
            'categories': categories,
            'selected_category': category,
            'selected_stock': stock_only,
            'selected_min_price': min_price,
            'selected_max_price': max_price,
            'selected_sort': sort_by
        }
    )

@is_authenticated
@customer_required
def add_to_wishlist(request,id):

    customer = Usermodel.objects.get(
        id=request.session['user_id']
    )

    product = ProductModel.objects.get(
        pid=id
    )

    WishlistModel.objects.create(
        customer=customer,
        product=product
    )

    return render(
        request,
        'success.html',
        {
            'message':'Product Added To Wishlist',
            "dashboard_url": "/flipazon/customer-dashboard/"
        }
    )
@is_authenticated
@customer_required
def view_wishlist(request):

    customer = Usermodel.objects.get(
        id=request.session['user_id']
    )

    wishlist = WishlistModel.objects.filter(
        customer=customer
    )

    return render(
        request,
        'wishlist.html',
        {
            'wishlist': wishlist
        }
    )

@is_authenticated
@customer_required
def remove_wishlist(request,id):

    item = WishlistModel.objects.get(
        id=id
    )

    item.delete()

    return render(
        request,
        'success.html',
        {
            'message':'Product Removed From Wishlist',
            "dashboard_url": "/flipazon/customer-dashboard/"
        }
    )

@is_authenticated
@customer_required
def add_to_cart(request,id):

    customer = Usermodel.objects.get(
        id=request.session['user_id']
    )

    product = ProductModel.objects.get(
        pid=id
    )

    cart_item = CartModel.objects.filter(
        customer=customer,
        product=product
    )

    if cart_item.exists():

        item = cart_item.first()

        item.quantity += 1

        item.save()

    else:

        CartModel.objects.create(
            customer=customer,
            product=product,
            quantity=1
        )

    return render(
        request,
        'success.html',
        {
            'message':'Product Added To Cart',
            "dashboard_url": "/flipazon/customer-dashboard/"
        }
    )

@is_authenticated
@customer_required
def view_cart(request):

    customer = Usermodel.objects.get(
        id=request.session['user_id']
    )

    cart = CartModel.objects.filter(
        customer=customer
    )

    return render(
        request,
        'cart.html',
        {
            'cart': cart
        }
    )


@is_authenticated
@customer_required
def remove_cart(request,id):

    cart_item = CartModel.objects.get(
        id=id
    )

    cart_item.delete()

    return render(
        request,
        'success.html',
        {
            'message':'Product Removed From Cart',
            "dashboard_url": "/flipazon/customer-dashboard/"
        }
    )

@is_authenticated
@customer_required
def place_order(request):

    customer = Usermodel.objects.get(
        id=request.session['user_id']
    )

    cart_items = CartModel.objects.filter(
        customer=customer
    )

    if not cart_items.exists():
        return render(
            request,
            'error.html',
            {'message': 'Your shopping cart is empty. Cannot place an order.'}
        )

    # Calculate grand total
    grand_total = sum(item.product.pprice * item.quantity for item in cart_items)

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        payment_method = request.POST.get("payment_method", "Cash on Delivery")
        
        selected_address = ""

        if address_id == "new":
            address_line1 = request.POST.get("address_line1")
            city = request.POST.get("city")
            state = request.POST.get("state")
            postal_code = request.POST.get("postal_code")
            country = request.POST.get("country", "India")
            
            if address_line1 and city and state and postal_code:
                addr = AddressModel.objects.create(
                    customer=customer,
                    address_line1=address_line1,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    country=country
                )
                selected_address = str(addr)
            else:
                return render(
                    request,
                    'error.html',
                    {'message': 'Please fill in all the shipping address fields.'}
                )
        elif address_id:
            try:
                addr = AddressModel.objects.get(id=address_id, customer=customer)
                selected_address = str(addr)
            except AddressModel.DoesNotExist:
                return render(
                    request,
                    'error.html',
                    {'message': 'Selected shipping address does not exist.'}
                )
        else:
            return render(
                request,
                'error.html',
                {'message': 'Please select or add a shipping address.'}
            )

        # Place orders
        for item in cart_items:
            OrderModel.objects.create(
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                total_price=item.quantity * item.product.pprice,
                shipping_address=selected_address,
                payment_method=payment_method
            )
            # Decrease product stock quantity
            item.product.pquantity = max(0, item.product.pquantity - item.quantity)
            item.product.save()

        cart_items.delete()

        return render(
            request,
            'success.html',
            {
                'message': 'Order Placed Successfully! Thank you for shopping with us.',
                "dashboard_url": "/flipazon/customer-dashboard/"
            }
        )

    # GET Request: render checkout screen
    first_item = cart_items.first()
    seller = first_item.product.seller if first_item else None
    addresses = AddressModel.objects.filter(customer=customer)
    
    return render(
        request,
        'checkout.html',
        {
            'cart': cart_items,
            'addresses': addresses,
            'grand_total': grand_total,
            'seller': seller
        }
    )

@is_authenticated
@customer_required
def view_orders(request):

    customer = Usermodel.objects.get(
        id=request.session['user_id']
    )

    orders = OrderModel.objects.filter(
        customer=customer
    )

    return render(
        request,
        'orders.html',
        {
            'orders': orders
        }
    )

@is_authenticated
@customer_required
def cancel_order(request,id):

    order = OrderModel.objects.get(
        id=id
    )

    order.delete()

    return render(
        request,
        'success.html',
        {
            'message':'Order Cancelled Successfully',
            "dashboard_url": "/flipazon/customer-dashboard/"
        }
    )
@is_authenticated
@customer_required
def add_review(request,id):

    if request.method == "POST":

        customer = Usermodel.objects.get(
            id=request.session['user_id']
        )

        product = ProductModel.objects.get(
            pid=id
        )

        ReviewModel.objects.create(
            customer=customer,
            product=product,
            rating=request.POST.get('rating'),
            review=request.POST.get('review')
        )

        return render(
            request,
            'success.html',
            {
                'message':'Review Added Successfully',
                "dashboard_url": "/flipazon/customer-dashboard/"
            }
        )

    return render(
        request,
        'review.html'
    )

from django.db.models import Avg

from django.db.models import Avg

@is_authenticated
@customer_required
def view_product_reviews(request,id):

    product = ProductModel.objects.get(
        pid=id
    )

    reviews = ReviewModel.objects.filter(
        product=product
    )

    avg_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    return render(
        request,
        'product_reviews.html',
        {
            'product': product,
            'reviews': reviews,
            'avg_rating': round(avg_rating,1) if avg_rating else 0
        }
    )

from django.shortcuts import redirect

def logout(request):

    request.session.flush()

    return redirect('/flipazon/login/')

@is_authenticated
def edit_profile(request):
    user_id = request.session.get('user_id')
    user = Usermodel.objects.get(id=user_id)
    addresses = AddressModel.objects.filter(customer=user) if user.role == "customer" else None
    
    if request.method == "POST":
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        if request.POST.get('password'):
            user.password = request.POST.get('password')
            
        if user.role == "seller":
            user.shop_name = request.POST.get('shop_name')
            user.shop_description = request.POST.get('shop_description')
            user.shop_address = request.POST.get('shop_address')
            user.upi_id = request.POST.get('upi_id')
            user.upi_qr_url = request.POST.get('upi_qr_url')
            if request.FILES.get('upi_qr_file'):
                user.upi_qr_file = request.FILES.get('upi_qr_file')
            
        user.save()
        
        back_url = "/flipazon/seller/" if user.role == "seller" else "/flipazon/customer-dashboard/"
        return render(
            request,
            'success.html',
            {
                'message': 'Profile Updated Successfully',
                'dashboard_url': back_url
            }
        )
        
    return render(
        request,
        'profile_edit.html',
        {
            'user': user,
            'addresses': addresses
        }
    )

@is_authenticated
@customer_required
def add_address(request):
    if request.method == "POST":
        customer = Usermodel.objects.get(id=request.session['user_id'])
        AddressModel.objects.create(
            customer=customer,
            address_line1=request.POST.get('address_line1'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country', 'India')
        )
        next_url = request.POST.get('next', '/flipazon/profile/edit/')
        return redirect(next_url)
    return redirect('/flipazon/profile/edit/')

@is_authenticated
@customer_required
def delete_address(request, id):
    customer = Usermodel.objects.get(id=request.session['user_id'])
    try:
        addr = AddressModel.objects.get(id=id, customer=customer)
        addr.delete()
    except AddressModel.DoesNotExist:
        pass
    return redirect('/flipazon/profile/edit/')

@is_authenticated
def product_detail(request, id):
    product = ProductModel.objects.get(pid=id)
    reviews = ReviewModel.objects.filter(product=product)
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'reviews': reviews,
            'avg_rating': avg_rating
        }
    )