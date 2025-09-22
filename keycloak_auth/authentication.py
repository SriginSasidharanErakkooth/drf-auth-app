import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class KeycloakAuthentication(BaseAuthentication):
    """
    Authenticate against Keycloak using Bearer token.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        # Introspect token with Keycloak
        introspect_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
        data = {
            "token": token,
            "client_id": settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        }

        response = requests.post(introspect_url, data=data)
        if response.status_code != 200:
            raise exceptions.AuthenticationFailed("Keycloak introspection failed")

        token_data = response.json()
        if not token_data.get("active"):
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        # You can return a Django user object mapped from Keycloak, here just returning None
        return (None, token)
