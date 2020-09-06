from rest_framework import generics
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class CreateUserAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        uri_path = self.request.get_full_path()
        data = self.request.data
        phone = data['phone']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']
        confirm_password = data['confirm_password']

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
            name = 'Superuser'
        elif 'create-staffuser' in uri_path:
            user = User.objects.create_staffuser(
                email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
            name = 'Staffuser'
        else:
            user = User.objects.create_user(
                email=email, first_name=first_name, last_name=last_name, phone=phone, password=password)
            name = 'User'

        user.save()
        return Response({'success': f"{name} created successfully"})
