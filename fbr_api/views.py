from os import stat
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework import status
from django.contrib.auth.models import User
from .models import FBR, RegisterUser
from .serialiazer import AddFRBSerializer, AddCnicSerializer, AllFRBSerializer, ChangePasswordSerializer, GetUserDetailserializer, IsSeenSerializer, RegisterSerializer, RegisterCnic, UserDetail
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
# Create your views here.


class GetAllFBR(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all().select_related()

    def get(self, request):
        queryset = FBR.objects.all()
        data_list = []
        for data in queryset:
            data = {
                "id": data.id,
                "title": data.title,
                "location": data.location,
                "district": data.district,
                "police_station": data.police_station,
                "catagory": data.catagory,
                "datetime": data.datetime,
                "mobile_number":data.mobile_number,
                "description": data.description,
                "is_seen": data.is_seen,
                "username": data.user.user.username,
                "created_by": data.user.user.first_name+" "+  data.user.user.last_name,
                "cnic_number": data.user.cnic

            }
            data_list.append(data)
        return Response(data_list)


class GetByCninFBR(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all()

    def get(self, request, pk):
        try:
            qs = RegisterUser.objects.get(cnic=pk)
            l = []
            # for i in qs:
            queryset = FBR.objects.filter(user=qs.id)
            # serializer_class = AllFRBSerializer(queryset)
            print(queryset)
            for fbr in queryset:
                data = {
                "id": fbr.id,
                "title": fbr.title,
                 }
                l.append(data)
            # ser = GetbyCNICSerializer(qs)
            return Response(l, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Error": "unable to get FBR due to some reasons"})

class GetCurrentUserFIR(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all()

    def get(self, request):
        try:
            l = []
            user_id = request.user.id
            # for i in qs:
            queryset = FBR.objects.filter(user=user_id)
            # serializer_class = AllFRBSerializer(queryset)
            print(queryset)
            for fbr in queryset:
                data = {
                "id": fbr.id,
                "title": fbr.title,
                 }
                l.append(data)
            # ser = GetbyCNICSerializer(qs)
            return Response(l, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Error": "unable to get FBR due to some reasons"})



class GetById(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AllFRBSerializer
    queryset = FBR.objects.all()

    def get(self, request, pk):
        try:
            queryset = FBR.objects.get(id=pk)
            data = {
                "id": queryset.id,
                "title": queryset.title,
                "location": queryset.location,
                "district": queryset.district,
                "police_station": queryset.police_station,
                "catagory": queryset.catagory,
                "datetime": queryset.datetime,
                "mobile_number":queryset.mobile_number,
                "description": queryset.description,
                "is_seen": queryset.is_seen,
                "username": queryset.user.user.username,
                "created_by": queryset.user.user.first_name+" "+  queryset.user.user.last_name,
                "cnic_number": queryset.user.cnic

            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Error": "unable to get FIR due to some reasons"})


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddCnicSerializer
    allowed_methods = ('POST',)

    def post(self, request, *args, **kwargs):
        current_user = request.user.id
        print(current_user)
        data = request.data
        data['user'] = current_user
        serializer = RegisterCnic(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class AddFBR(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
            return Response({"Error": "unalbe to register FBR"})


class GetUserDetail(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetUserDetailserializer

    def get(self, request):
        user = request.user.id
        print(self.request.user)
        try:
            queryset = RegisterUser.objects.get(user=user)
            data = {
                'id': queryset.id,
                'first_name': queryset.user.first_name,
                'last_name': queryset.user.last_name,
                'username': queryset.user.username,
                'email': queryset.user.email,
                'superuser': queryset.user.is_superuser,
                'cnic': queryset.cnic

            }
            return Response(data)
        except Exception as e:
            print(e)
            return Response({"Error": "CNIC not available"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateisSeen(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = IsSeenSerializer
    allowed_methods = ('PATCH',)

    def update(self, request, pk, *args, **kwargs):
        try:
            qs = FBR.objects.get(id=pk)
            ser = IsSeenSerializer(instance=qs, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'unable to update'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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

class CheckCNIC(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddCnicSerializer
    def get(self, request):
        user = request.user.id
        print(self.request.user)
        try:
            queryset = RegisterUser.objects.get(user=user)
            data = {
                'cnic': queryset.cnic
            }
            return Response(data)
        except Exception as e:
            print(e)
            return Response({"Error": "CNIC not available"}, status=status.HTTP_400_BAD_REQUEST)
