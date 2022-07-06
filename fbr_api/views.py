from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView , CreateAPIView ,UpdateAPIView
from rest_framework import status
from django.contrib.auth.models import User
from .models import FBR, RegisterUser
from .serialiazer import AddFRBSerializer, AddCnicSerializer, AllFRBSerializer, ChangePasswordSerializer, GetUserDetailserializer, IsSeenSerializer, RegisterSerializer ,RegisterCnic
from fbr_api import serialiazer

# Create your views here.

class GetAllFBR(ListAPIView):
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all()

class GetByCninFBR(ListAPIView):
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all()
     
    def get(self, request , pk):
        try:
            qs = RegisterUser.objects.get(cnic=pk)
            l = []
            # for i in qs:
            queryset = FBR.objects.filter(user=qs.id)
                # serializer_class = AllFRBSerializer(queryset)
            print(queryset)
            data = {}
            for fbr in queryset:
                data['title'] = fbr.title
                data['description'] = fbr.description
            print(data) 
            l.append(data)
            # ser = GetbyCNICSerializer(qs)
            return Response(l , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Error":"unable to get FBR due to some reasons"})


class GetById(ListAPIView):
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all()
     
    def get(self, request , pk):
        try:
            queryset = FBR.objects.get(id=pk)
            serializer_class = AllFRBSerializer(queryset)
            return Response(serializer_class.data , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Error":"unable to get FBR due to some reasons"})





class RegisterUserByFrontend(CreateAPIView):
    serializer_class = RegisterSerializer
    allowed_methods = ('POST',)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
            print('Error', data.keys())
        return Response(data)


class AddCnic(CreateAPIView):
    serializer_class = AddCnicSerializer
    allowed_methods = ('POST',)

    def post(self, request, *args, **kwargs):
        serializer = AddCnicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors )

class AddFBR(CreateAPIView):
    serializer_class = AddFRBSerializer
    queryset = FBR.objects.all()

    def post(self, request, *args, **kwargs):
        current_user = request.user.id
        print(current_user)
        data = request.data
        data['user'] = current_user
        try:
            serializer = AllFRBSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"Error" : "unalbe to register FBR"})


class GetUserDetail(ListAPIView):
    serializer_class = GetUserDetailserializer
    def get_queryset(self):
        user = self.request.user.id
        print(user)
        queryset = User.objects.filter(id=user)
        return queryset

class UpdateisSeen(UpdateAPIView):
    serializer_class = IsSeenSerializer
    allowed_methods = ('PATCH',)

    def update(self, request, pk , *args , **kwargs):
        try:
            qs = FBR.objects.get(id=pk)
            ser = IsSeenSerializer(instance=qs , data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data , status=status.HTTP_200_OK)
            return Response(ser.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error':'unable to update'} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(UpdateAPIView):

        serializer_class = ChangePasswordSerializer
        model = User
        allowed_methods = ('PATCH',)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
