from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login

from .serializeras import MerchantRegisterSerializer, LoginSerializer, MerchantChangePassword, MerchantChangePasswordSendEmailSerializer, MerchantResetPasswordSerializer

# Create your views here.

from rest_framework_simplejwt.tokens import RefreshToken

#Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class MerchantRegisterView(APIView):
    def post(self, request):
        serializer = MerchantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'Token':token,'msg':'Register Success!!!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                login(request,user)
                return Response({'Token':token,'msg':'Login Success!!!'},status=status.HTTP_200_OK)
        return Response({"msg":"Email or Password is not valid!!!"},status=status.HTTP_400_BAD_REQUEST)
    

class MerchantChangePasswordView(APIView):
    def post(self, request):
        serializer = MerchantChangePassword(data=request.data,context={'user':request.user})
        if serializer.is_valid():

            return Response({'msg':"password changed successfuly!!!"})
        return Response({'msg':serializer.errors})
    
class MerchantPasswordChangeEmailSendView(APIView):
    def post(self, request):
        serializer = MerchantChangePasswordSendEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password change credential wos send, check your email'})
        return Response(serializer.errors)
    
class MerchantResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = MerchantResetPasswordSerializer(data=request.data, context={'uid':uid,'token':token})
        if serializer.is_valid():
            return Response({'msg':'success'})
        return Response(serializer.errors)