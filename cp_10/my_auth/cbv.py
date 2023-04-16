from rest_framework.views import APIView, Response
from .serializers import UserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, ResetPassword
from django.core.mail import send_mail
from django import template
import uuid
from datetime import datetime, timezone

RESET_PASSWORD_TOKEN_EXPIRATION_PERIOD = 1 * 60 * 60


class RegisterUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.user.username)
        user.set_password(data['new_password'])
        user.save()
        user_serializer = UserSerializer(user)
        return Response(data=user_serializer.data, status=200)


class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = data['email']
        token = uuid.uuid4()
        reset_password = ResetPassword(email=email, token=token)
        reset_password.save()
        #####
        email_template = template.loader.get_template('my_auth/reset-password-email.html')
        email_content = email_template.render({'FRONTEND_RESET_PASSWORD_URL': 'http://localhost:5500/reset-password',
                                               'TOKEN': token})
        try:
            send_mail(subject='Reset Your Password', message='', html_message=email_content,
                      from_email='settings.EMAIL_HOST_USER', recipient_list=[email], fail_silently=False)
            return Response({'message': "Email is sent! Please check"}, status=200)
        except:
            return Response({'message': "Internal server error"}, status=500)
        ####


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, token):
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        reset_password = ResetPassword.objects.get(token=token)
        email = reset_password.email
        created_at = reset_password.created_at
        user = User.objects.get(email=email)

        if (datetime.now(timezone.utc) - created_at).total_seconds() > RESET_PASSWORD_TOKEN_EXPIRATION_PERIOD:
            reset_password.delete()
            return Response({'message': 'Token is expired, please sent forgot password request again!'}, status=404)
        else:
            user.set_password(data['new_password'])
            user.save()
            reset_password.delete()
            return Response({'message': 'Users password updated successfully!'}, status=200)

