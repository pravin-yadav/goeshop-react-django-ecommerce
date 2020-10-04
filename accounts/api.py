from rest_framework import generics
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.authtoken.models import Token


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, *args, **kwargs):
        username = kwargs.get('username')
        if username is None:
            return None
        else:
            try:
                user = User.objects.get(Q(email=username) | Q(phone=username))
                pwd_valid = user.check_password(password)
                if pwd_valid:
                    return user
                else:
                    return None
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class CreateUserAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uri_path = self.request.get_full_path()
        data = self.request.data
        phone = data['phone']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']
        confirm_password = data['confirm_password']
        userdata = {}
        if password != confirm_password:
            return Response({'error': 'Password do not match'})

        if len(password) < 6:
            return Response({'error': 'Password must be atleast 6 characters'})

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exist'})

        if User.objects.filter(phone=phone).exists():
            return Response({'error': 'Phone number already exist'})

        if 'create-superuser' in uri_path:
            user = User.objects.create_superuser(
                email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
            name = 'superuser'
            token, created = Token.objects.get_or_create(user=user)

        elif 'create-staffuser' in uri_path:
            user = User.objects.create_staffuser(
                email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
            name = 'staffuser'
            token, created = Token.objects.get_or_create(user=user)

        else:
            user = User.objects.create_user(
                email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
            name = 'user'
            token, created = Token.objects.get_or_create(user=user)

        userdata['success'] = True
        userdata['name'] = f"{first_name} {last_name}"
        userdata['email'] = email
        userdata['phone'] = phone
        userdata['token'] = token.key
        userdata['role'] = name

        if user:
            user.save()
            return Response({'data': userdata})
