import jwt
from django.shortcuts import redirect
from .models import Usermodel

SECRET_KEY = "django-insecure-x)@i5h6la(0z2ri&s(4%33gypfet75g+gep2%o5wbvnab(rt)0"

def is_authenticated(func):

    def wrapper(request,*args,**kwargs):

        token = request.session.get('token')

        if not token:
            return redirect('/flipazon/login/')

        try:

            decoded_token = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            user = Usermodel.objects.filter(
                email=decoded_token['email']
            )

            if user.exists():

                request.current_user = user.first()

                return func(
                    request,
                    *args,
                    **kwargs
                )

            return redirect('/flipazon/login/')

        except:

            return redirect('/flipazon/login/')

    return wrapper

def seller_required(func):

    def wrapper(request,*args,**kwargs):

        if request.session.get('role') != 'seller':

            return redirect('/flipazon/login/')

        return func(
            request,
            *args,
            **kwargs
        )

    return wrapper

def customer_required(func):

    def wrapper(request,*args,**kwargs):

        if request.session.get('role') != 'customer':

            return redirect('/flipazon/login/')

        return func(
            request,
            *args,
            **kwargs
        )

    return wrapper

def admin_required(func):

    def wrapper(request,*args,**kwargs):

        if request.session.get('role') != 'admin':

            return redirect('/flipazon/login/')

        return func(
            request,
            *args,
            **kwargs
        )

    return wrapper