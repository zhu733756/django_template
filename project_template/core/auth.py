from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.conf import settings

import json

expiring_hour = settings.TOKEN_LIFETIME or 24


#auth
class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()

        if token.created < utc_now - timedelta(hours=expiring_hour):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token


from rest_framework.authtoken.views import ObtainAuthToken


#views
class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            utc_now = datetime.utcnow()
            if not created and token.created < utc_now - timedelta(
                    hours=expiring_hour):
                Token.objects.filter(user=user).update(
                    key=token.generate_key(), created=datetime.now())

            #return Response({'token': token.key})
            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
