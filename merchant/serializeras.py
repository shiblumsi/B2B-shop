from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers

from .models import MerchantUser
from .utils import Util

class MerchantRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = MerchantUser
        fields = ['email','password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password not match")
        return attrs
    
    def create(self, validated_data):
        print('dataaaaa',validated_data)
        return MerchantUser.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class MerchantChangePassword(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise ValueError("password not matched!!!")
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return attrs
    
class MerchantChangePasswordSendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)

    def validate(self, attrs):
        email = attrs.get('email')
        if MerchantUser.objects.filter(email=email).exists():
            user = MerchantUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            u = smart_str(urlsafe_base64_decode(uid))
            print('Encoded UID:',uid,u)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token:',token)
            link =  'http://127.0.0.1:8000/reset/'+uid+'/'+token
            print('Password Reset Link:',link)
            data = {
                'subject':'Reset Password Link',
                'body':"click Following link to Reset Your Password:"+link,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs

        else:
            raise serializers.ValidationError("Your Email is not Authorized!!!")
        

class MerchantResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            if password != password2:
                raise ValueError("password not matched!!!")
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = MerchantUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token may not Valid or Expired!!!")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not Valid or Expired!!!")
       